from ctypes import sizeof

from ab_translator.data_structures import LOGAB_HDR, PAYLOAD_HDR, LOGAB, PAYLOAD_HDR_SIZE, EXTDTRLS, EXTDTAB, EXTDTCOMMAB
from ab_translator.msg import Msg
from ab_translator.constants import *
from ab_translator.ab_race import ABRaceTranslator
from ab_translator.ab_cancel import ABCancelTranslator
from ab_translator.msg_error import MsgError


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

def translate_from_bytes(hex_data: bytes, tuple_output: bool = False):
    # Parse the Payload headers
    pHdr = PAYLOAD_HDR.from_buffer_copy(hex_data)

    # Parse the LOGAB headers
    logabHdr = LOGAB_HDR.from_buffer_copy(hex_data, PAYLOAD_HDR_SIZE + pHdr.extra_data_len)

    # Parse the LOGAB including LOGAB_HDR and LOGAB_DATA. 
    # Padding the hex_data if the length is less than the size of LOGAB
    chunk = hex_data[PAYLOAD_HDR_SIZE + pHdr.extra_data_len:]
    pMlog = LOGAB.from_buffer_copy(chunk.ljust(sizeof(LOGAB), b'\x00'))

    # Initialize the Msg object
    pMsg = get_msg_obj(pHdr, logabHdr, hex_data)

    pMlog.hdr.custSessIdd = pHdr.cust_session_id

    msg_error = MsgError(pMlog, pMsg)
    if msg_error.has_error():
        if tuple_output:
            return get_tuple_header(pHdr) + msg_error.get_error_to_tuple()
        return get_string_header(pHdr) + msg_error.get_error_to_string()

    if pMsg.m_iMsgCode == LOGAB_CODE_RAC:
        translator = ABRaceTranslator(pMlog, pMsg)
    elif pMsg.m_iMsgCode == LOGAB_CODE_CAN:
        translator = ABCancelTranslator(pMlog, pMsg)
    else:
        raise Exception("Unknown message code")
    
    if tuple_output:
        return get_tuple_header(pHdr) + translator.translate_to_tuple()
    return get_string_header(pHdr) + translator.translate_to_string()

    
def translate(input_data: str, tuple_output: bool = False) -> str:
    hex_data = bytes.fromhex(input_data)
    return translate_from_bytes(hex_data, tuple_output)


def get_string_header(pHdr: PAYLOAD_HDR) -> str:
    return (
        f"{pHdr.system_id}@|@"
        f"{pHdr.business_date}@|@"
        f"{pHdr.activity_id:d}@|@"
        f"{pHdr.enquiry_status}@|@"
        f"{pHdr.activity_nature}@|@"
    )


def get_tuple_header(pHdr: PAYLOAD_HDR) -> tuple[int, str, int, int, int]:

    # header_schema = StructType([
    #     StructField("headerSystemID", LongType()),
    #     StructField("headerBusinessDate", StringType()),
    #     StructField("headerActivityID", LongType()),
    #     StructField("headerEnquiryStatus", LongType()),
    #     StructField("headerActivityNature", LongType())
    # ])

    return (
        pHdr.system_id,
        f"{pHdr.business_date:08d}",
        pHdr.activity_id,
        pHdr.enquiry_status,
        pHdr.activity_nature
    )