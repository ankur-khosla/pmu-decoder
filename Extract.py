from ctypes import sizeof, c_ulonglong, c_uint, c_ushort
from data_structures import LOGAB_HDR, PAYLOAD_HDR, LOGAB, PAYLOAD_HDR_SIZE, LOGAB_DATA, EXTDTRLS, EXTDTAB, EXTDTCOMMAB
from Msg import Msg
from constants import *


input_data = "14000000D3B334010029470902000000428A143F01000000000000000005001C001E0000002C0A5F6500000000CC000000000000002C0A5F6500000000D3B33401ED000600000000B0650300E90600002C45F2000000000000000000000000CC002C0A5F65FE284709020000004F6E000005000000009B5F140000000120D3B33401000000000000000000009210190001000000428A143F0100000000000000000000000000E906000000000000000000000000000000000000010000FE0500000500000000000000001E0000007017000000000000D3B334010400080505D3B334010201FC8FAEA41E01000000000000000000000F0000000000004000000000000020040000000000000000000000000000000000000000000000000000000000000000000000000000010000"
# input_data = "14000000D3B33401032E470902000000578A143F01000000000000000004001D001E000000550B5F65000000009700000000000000550B5F6500000000D3B33401ED00060000000F9E590300830000001745F20000000000000000000000009700550B5F65012E4709020000007557000005000000000858140000004120D3B33401000000000000000000002C0A190001000000578A143F01000000000000000000000000008300000000000000000000000000000000000000020000D2050000050000000000000000C8020180402CCA0000000000D3B334010A00080605D3B3340101033E16B0A41E01000000000000000000000F080F0000000200000000000000FCFF000000000000FE0100000000000000000000000000000220000000000000FCDF000000000000010002"

hex_data = bytes.fromhex(input_data)

print("============================= PAYLOAD HEADER =============================")
pHdr = PAYLOAD_HDR.from_buffer_copy(hex_data)

payLoadOutput = (
    f"{pHdr.system_id}@|@"
    f"{pHdr.business_date}@|@"
    f"{pHdr.activity_id:d}@|@"   # explicitly format as unsigned decimal
    f"{pHdr.enquiry_status}@|@"
    f"{pHdr.activity_nature}@|@"
)

print("============================= LOGAB HDR =============================")
logabHdr = LOGAB_HDR.from_buffer_copy(hex_data, PAYLOAD_HDR_SIZE + pHdr.extra_data_len)

print("============================= LOGAB DATA =============================")
LOGAB_SIZE = sizeof(LOGAB)
offset = PAYLOAD_HDR_SIZE + pHdr.extra_data_len
chunk = hex_data[offset:]

# Padding the chunk to the size of LOGAB
logAb = LOGAB.from_buffer_copy(chunk.ljust(LOGAB_SIZE, b'\x00'))
logabData = logAb.data

# ============  ExtractMgr::GetMsgObj(unsigned char *binArr, PAYLOAD_HDR *pHdr, LOGAB *pMlog)============

def split_int_yyyymmdd(value: int) -> tuple[int, int, int]:
    tmp_str = f"{value:08d}"
    return int(tmp_str[:4]), int(tmp_str[4:6]), int(tmp_str[6:8])


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

plExtData_Buf = hex_data[PAYLOAD_HDR_SIZE : PAYLOAD_HDR_SIZE + pHdr.extra_data_len]

if pMsg.m_iMsgCode == LOGAB_CODE_RAC: # ABRace 
    extDTRLS = EXTDTRLS.from_buffer_copy(plExtData_Buf)
    pMsg.m_iMsgErrwu = extDTRLS.extDTAB.extdtcomm.acterrwu
    pMsg.m_iMsgTime = extDTRLS.extDTAB.extdtcomm.actts # Not translated from t64 to t32
    pMsg.txnidd = extDTRLS.extDTAB.txnidd
    pMsg.m_iMsgSellTime = extDTRLS.sellTime # Not translated from t64 to t32
    pMsg.m_MsgBizDate = extDTRLS.bizdatelu
    pMsg.m_iMsgYear, pMsg.m_iMsgMonth, pMsg.m_iMsgDay = split_int_yyyymmdd(extDTRLS.bizdatelu)
    
elif pMsg.m_iMsgCode == LOGAB_CODE_CAN: # ABCancel
    extDTAB = EXTDTAB.from_buffer_copy(plExtData_Buf)
    pMsg.m_iMsgErrwu = extDTAB.extdtcomm.acterrwu
    pMsg.m_iMsgTime = extDTAB.extdtcomm.actts # Not translated from t64 to t32
    pMsg.txnidd = extDTAB.txnidd

else:
    extDTComm = EXTDTCOMMAB.from_buffer_copy(plExtData_Buf)
    pMsg.m_iMsgErrwu = extDTComm.acterrwu
    pMsg.m_iMsgTime = extDTComm.actts # Not translated from t64 to t32

# ============  End of ExtractMgr::GetMsgObj(unsigned char *binArr, PAYLOAD_HDR *pHdr, LOGAB *pMlog) ============

if logabHdr.prelog1 != 0:
    raise Exception("Obsolete message")

# ============ char * ABMsgTranslator::TranslateHeader(const Msg *pMsg) ============

if pMsg.m_iMsgErrwu != 0:
    raise Exception("Error Happened: m_iMsgErrwu!=0, omitted getting Error (ABMsgTranslator::GetError) logic for now")

if logabHdr.prelog1 != 0 or logabHdr.laterpy1 != 0 or logabHdr.timeout1 != 0 or logabHdr.train1 != 0:
    raise Exception("Error Happened: prelog1!=0 or laterpy!=0 or timeout1!=0 or train!=0, omitted getting Error (ABMsgTranslator::GetError) logic for now")

# ============  End of ABMsgTranslator::TranslateHeader(const Msg *pMsg) ============


# ============ char * ABMsgTranslator::TranslateAction(const Msg *pMsg) ============
# ============ char * ABRace::TranslateAction(const Msg *pMsg) ============ 
# 先实现ABRace逻辑

# print(logabHdr.lgslu)
# print(logAb.hdr.lgslu)

# print(c_uint(logabHdr.lgslu).value)

import abrace
abrace = abrace.ABRace()
print(payLoadOutput +abrace.packHeader("ABRace", logAb, pMsg) + abrace.translate_action(pMsg, logAb))


# print(logAb.hdr.noFlush1)
# print(c_ushort(logAb.hdr.noFlush1).value)








