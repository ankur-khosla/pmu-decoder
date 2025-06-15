from ctypes import sizeof
from ab_translator.data_structures import LOGAB_HDR, PAYLOAD_HDR, LOGAB, PAYLOAD_HDR_SIZE, EXTDTRLS, EXTDTAB, EXTDTCOMMAB
from ab_translator.msg import Msg
from ab_translator.constants import *
import ab_translator.ab_translator as ab_translator_module


def split_int_yyyymmdd(value: int) -> tuple[int, int, int]:
    tmp_str = f"{value:08d}"
    return int(tmp_str[:4]), int(tmp_str[4:6]), int(tmp_str[6:8])


def get_msg_obj(pHdr: PAYLOAD_HDR, logabHdr: LOGAB_HDR, hex_data: bytes) -> Msg:
    pMsg = Msg()
    pMsg.m_iMsgYear, pMsg.m_iMsgMonth, pMsg.m_iMsgDay = split_int_yyyymmdd(logabHdr.bizdatelu)

    if pHdr.system_id == ACP01:
        pMsg.m_iSysName = "ACP01"
    elif pHdr.system_id == ACP02:
        pMsg.m_iSysName = "ACP02"
    else:
        pMsg.m_iSysName = "Unknown"

    pMsg.m_iSysNo = pHdr.system_id
    pMsg.SellingDate = pHdr.business_date
    pMsg.m_iMsgSize = logabHdr.sizew
    pMsg.m_iMsgCode = logabHdr.codewu

    plExtData_Buf = hex_data[PAYLOAD_HDR_SIZE: PAYLOAD_HDR_SIZE + pHdr.extra_data_len]

    if pMsg.m_iMsgCode == LOGAB_CODE_RAC:
        extDTRLS = EXTDTRLS.from_buffer_copy(plExtData_Buf)
        pMsg.m_iMsgErrwu = extDTRLS.extDTAB.extdtcomm.acterrwu
        pMsg.m_iMsgTime = extDTRLS.extDTAB.extdtcomm.actts
        pMsg.txnidd = extDTRLS.extDTAB.txnidd
        pMsg.m_iMsgSellTime = extDTRLS.sellTime
        pMsg.m_MsgBizDate = extDTRLS.bizdatelu
        pMsg.m_iMsgYear, pMsg.m_iMsgMonth, pMsg.m_iMsgDay = split_int_yyyymmdd(extDTRLS.bizdatelu)

    elif pMsg.m_iMsgCode == LOGAB_CODE_CAN:
        extDTAB = EXTDTAB.from_buffer_copy(plExtData_Buf)
        pMsg.m_iMsgErrwu = extDTAB.extdtcomm.acterrwu
        pMsg.m_iMsgTime = extDTAB.extdtcomm.actts
        pMsg.txnidd = extDTAB.txnidd

    else:
        extDTComm = EXTDTCOMMAB.from_buffer_copy(plExtData_Buf)
        pMsg.m_iMsgErrwu = extDTComm.acterrwu
        pMsg.m_iMsgTime = extDTComm.actts

    return pMsg


def translate(input_data: str) -> str:
    hex_data = bytes.fromhex(input_data)

    # Parse headers
    pHdr = PAYLOAD_HDR.from_buffer_copy(hex_data)
    logabHdr = LOGAB_HDR.from_buffer_copy(hex_data, PAYLOAD_HDR_SIZE + pHdr.extra_data_len)

    chunk = hex_data[PAYLOAD_HDR_SIZE + pHdr.extra_data_len:]
    logAb = LOGAB.from_buffer_copy(chunk.ljust(sizeof(LOGAB), b'\x00'))

    pMsg = get_msg_obj(pHdr, logabHdr, hex_data)

    if logabHdr.prelog1 != 0:
        raise Exception("Obsolete message")
    if pMsg.m_iMsgErrwu != 0:
        raise Exception("Error: m_iMsgErrwu != 0")
    if logabHdr.prelog1 != 0 or logabHdr.laterpy1 != 0 or logabHdr.timeout1 != 0 or logabHdr.train1 != 0:
        raise Exception("Error: abnormal LOGAB flags set")

    ab_translator = ab_translator_module.ABTranslator()
    payLoadOutput = (
        f"{pHdr.system_id}@|@"
        f"{pHdr.business_date}@|@"
        f"{pHdr.activity_id:d}@|@"
        f"{pHdr.enquiry_status}@|@"
        f"{pHdr.activity_nature}@|@"
    )

    if pMsg.m_iMsgCode == LOGAB_CODE_RAC:
        return payLoadOutput + ab_translator.packHeader(logAb, pMsg) + ab_translator.translate_abrace(pMsg, logAb)
    elif pMsg.m_iMsgCode == LOGAB_CODE_CAN:
        return payLoadOutput + ab_translator.packHeader(logAb, pMsg) + ab_translator.translate_abcancel(pMsg, logAb)
    else:
        raise Exception("Unknown message code")