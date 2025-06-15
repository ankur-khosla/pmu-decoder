import re

# 1) the fields in the exact order after the leading "0@|@"
field_names = [
    "m_iMsgCode",
    "m_sSysName",
    "m_iMsgOrderNo",
    "m_sSellingDate",
    "m_iMsgSize",
    "m_iMsgCode",       # duplicate on purpose
    "m_iErrCode",
    "m_iTrapCode",
    "m_iStaffNo",
    "m_iLogTermNo",
    "m_iAcctNo",
    "m_iFileNo",
    "m_iBlockNo",
    "m_iOverflowNo",
    "m_iOffsetUnit",
    "m_iTranNo",
    "m_sTime",
    "m_iLastLogSeq",
    "m_iMsnNo",
    "m_iExtSysType",
    "m_iCatchUp",
    "m_iBtExcept",
    "m_iOtherSys",
    "m_iPreLog",
    "m_iTimeout",
    "m_iLateReply",
    "m_iBcsMsg",
    "m_iRcvMsg",
    "m_iOverFlow",
    "m_iEscRel",
    "m_iNoFlush",
    "m_iTrainAcct",
    "m_iSessionInfo",
    "m_iSourceType",
    "m_cVoiceFENo",
    "m_sTerminalNo",
    "m_iVoiceLocId",
    "m_iDidCitNo",
    "m_cDidPseTermNo",
    "m_cDidFENo",
    "m_sDidCitType",
    "m_iCBCenterNo",
    "m_iCBWindowNo",
    "m_iCBLogTermNo",
    "m_cCBSysNo",
    "m_iOldCenterNo",
    "m_iOldWindowNo",
    "m_iOldChanNo",
    "m_cOldSysNo",
    "m_cPolFileNo",
    "m_iPolOffsetNo",
    "m_cMatNo",
    "m_iBatchDep",
    "m_iCallSeq",        # printed via AddField64 when errCode==0
    "m_iTerminalType",   # printed when msgCode!=202
]

# example strings (with %…% markers in the “got” version)
expected = """0@|@6@|@ACP01~|~0~|~23-Nov-2023~|~237~|~6~|~0~|~0~|~222640~|~1769~|~15877420~|~0~|~0~|~0~|~0~|~204~|~23-Nov-2023 16:15:40~|~155658494~|~28239~|~0~|~1~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~5~|~0~|~ ~|~0~|~0~|~155~|~95~|~IOSBS~|~0~|~0~|~0~|~0~|~0~|~0~    |~0~ |~0~|~ ~|~0~    |~5353278018"""
got      = """0@|@6@|@ACP01~|~0~|~23-Nov-2023~|~237~|~6~|~0~|~0~|~222640~|~1769~|~15877420~|~0~|~0~|~0~|~0~|~204~|~23-Nov-2023 16:15:40~|~155658494~|~28239~|~0~|~1~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~5~|~0~  |~0~ |~0~    |~0~|~0~|~0~|~0~|~0~|~24475~|~20~|~0~|~0~|~24475~|~20~|~0~|~0~|~0~|~~|~0~|~5353278018~|~"""

def split_and_clean(s: str):
    # strip out the %10%, %20%, etc.
    cleaned = re.sub(r'%\d+%', '', s)
    # remove the leading "0@|@" and split by "~|~"
    return cleaned.split('@|@', 1)[1].split('~|~')

exp_fields = split_and_clean(expected)
got_fields = split_and_clean(got)

# 4) Compare and print mismatches by name
for name, e_val, g_val in zip(field_names, exp_fields, got_fields):
    if e_val != g_val:
        print(f"{name}: expected={e_val!r}, got={g_val!r}")