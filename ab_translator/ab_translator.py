import ctypes

from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime

from ab_translator.constants import *
from ab_translator.data_structures import LOGAB
from ab_translator.msg import Msg

@dataclass
class HeaderData:
    """Data class for packHeader output"""
    # Initial fields with @|@ delimiter
    m_iMsgCode: int = 0
        
    # Main fields with ~|~ delimiter
    m_iSysNo: int = 0
    m_iMsgOrderNo: int = 0
    m_sSellingDate: datetime = datetime.fromtimestamp(0)
    m_sSysName: str = ""
    m_iMsgSize: int = 0
    m_iMsgCode: int = 0
    m_iErrCode: int = 0
    m_iTrapCode: int = 0
    m_iStaffNo: int = 0
    m_iLogTermNo: int = 0
    m_iAcctNo: int = 0
    m_iFileNo: int = 0
    m_iBlockNo: int = 0
    m_iOverflowNo: int = 0
    m_iOffsetUnit: int = 0
    m_iTranNo: int = 0
    m_iLastLogSeq: int = 0
    m_iMsnNo: int = 0
    m_iBatchDep: int = 0
    m_cMatNo: str = ""    
    m_iExtSysType: int = 0
    m_iCatchUp: int = 0
    m_iBtExcept: int = 0
    m_iOtherSys: int = 0
    m_iPreLog: int = 0
    m_iTimeout: int = 0
    m_iLateReply: int = 0
    m_iBcsMsg: int = 0
    m_iRcvMsg: int = 0
    m_iOverFlow: int = 0
    m_iEscRel: int = 0
    m_iNoFlush: int = 0
    m_iTrainAcct: int = 0
    m_iSessionInfo: int = 0
    m_iSourceType: int = 0
    m_sTime: datetime = datetime.fromtimestamp(0)
    m_iMatNo: int = 0
    m_cVoiceFENo: int = 0
    m_iVoiceTermNo: int = 0
    m_iVoiceLocId: int = 0
    m_sTerminalNo: str = ""
    m_iDidCitNo: int = 0
    m_cDidPseTermNo: int = 0
    m_cDidFENo: int = 0
    m_sDidCitType: str = ""
    m_iCBCenterNo: int = 0
    m_iCBWindowNo: int = 0
    m_iCBLogTermNo: int = 0
    m_cCBSysNo: int = 0
    m_iOldCenterNo: int = 0
    m_iOldWindowNo: int = 0
    m_iOldChanNo: int = 0
    m_cOldSysNo: int = 0
    m_cPolFileNo: int = 0
    m_iPolOffsetNo: int = 0
    m_iCallSeq: int = 0
    m_iTerminalType: int = 0

class ABTranslator:
    def __init__(self, pMlog: LOGAB, pMsg: Msg):
        self.m_pMlog = pMlog
        self.m_pMsg = pMsg

        # Initialize all the fields that were in the C++ code
        self.data_header = HeaderData()        
        self.m_iLoggerMsgOrderNo = 0
        self.terminal_type_matrix = defaultdict(lambda: defaultdict(int))

        # Load Values to HeaderData
        self.packHeader()
    
    def get_terminal_type(self):

        pMlog = self.m_pMlog
        pMsg = self.m_pMsg

        # Only handle CB_BT source messages
        if pMlog.hdr.source.srcTypebu != LOGAB_SRC_CB_BT:
            return 0

        centre = pMlog.hdr.source.data.cbBt.centrelu
        window = pMlog.hdr.source.data.cbBt.windowwu

        # On account access, record input mode
        if pMlog.hdr.codewu == LOGAB_CODE_ACA:
            mode = pMlog.data.bt.aca.dev.cb.svt1
            self.terminal_type_matrix[centre][window] = mode

        # Retrieve stored mode
        if centre not in self.terminal_type_matrix:
            return 2
        if window not in self.terminal_type_matrix[centre]:
            return 2
        ttype = self.terminal_type_matrix[centre][window]

        # Normalize: only 0 or 1 preserved, else map to 2
        if ttype not in (0, 1):
            return 2
        return ttype

    def translate_header_to_string(self) -> str:
        """Convert HeaderData to formatted string"""
        # Handle last_log_seq with conditional logic
        last_log_seq_val = self.data_header.m_iLastLogSeq if self.data_header.m_iLastLogSeq < 2147483647 else 2147483647
        
        # Build initial part with @|@ delimiter
        output_str = f"0@|@{self.data_header.m_iMsgCode}@|@"
        
        # Build main part with ~|~ delimiter
        output_str += (
            f"{self.data_header.m_sSysName}~|~"
            f"{self.data_header.m_iMsgOrderNo}~|~"
            f"{self.data_header.m_sSellingDate.strftime("%d-%b-%Y")}~|~"
            f"{self.data_header.m_iMsgSize}~|~"
            f"{self.data_header.m_iMsgCode}~|~"
            f"{self.data_header.m_iErrCode}~|~"
            f"{self.data_header.m_iTrapCode}~|~"
            f"{self.data_header.m_iStaffNo}~|~"
            f"{self.data_header.m_iLogTermNo}~|~"
            f"{self.data_header.m_iAcctNo}~|~"
            f"{self.data_header.m_iFileNo}~|~"
            f"{self.data_header.m_iBlockNo}~|~"
            f"{self.data_header.m_iOverflowNo}~|~"
            f"{self.data_header.m_iOffsetUnit}~|~"
            f"{self.data_header.m_iTranNo}~|~"
            f"{self.data_header.m_sTime.strftime("%d-%b-%Y %H:%M:%S")}~|~"
            f"{last_log_seq_val}~|~"
            f"{self.data_header.m_iMsnNo}~|~"
            f"{self.data_header.m_iExtSysType}~|~"
            f"{self.data_header.m_iCatchUp}~|~"
            f"{self.data_header.m_iBtExcept}~|~"
            f"{self.data_header.m_iOtherSys}~|~"
            f"{self.data_header.m_iPreLog}~|~"
            f"{self.data_header.m_iTimeout}~|~"
            f"{self.data_header.m_iLateReply}~|~"
            f"{self.data_header.m_iBcsMsg}~|~"
            f"{self.data_header.m_iRcvMsg}~|~"
            f"{self.data_header.m_iOverFlow}~|~"
            f"{self.data_header.m_iEscRel}~|~"
            f"{self.data_header.m_iNoFlush}~|~"
            f"{self.data_header.m_iTrainAcct}~|~"
            f"{self.data_header.m_iSessionInfo}~|~"
            f"{self.data_header.m_iSourceType}~|~"
            f"{self.data_header.m_cVoiceFENo}~|~"
            f"{self.data_header.m_sTerminalNo}~|~"
            f"{self.data_header.m_iVoiceLocId}~|~"
            f"{self.data_header.m_iDidCitNo}~|~"
            f"{self.data_header.m_cDidPseTermNo}~|~"
            f"{self.data_header.m_cDidFENo}~|~"
            f"{self.data_header.m_sDidCitType}~|~"
            f"{self.data_header.m_iCBCenterNo}~|~"
            f"{self.data_header.m_iCBWindowNo}~|~"
            f"{self.data_header.m_iCBLogTermNo}~|~"
            f"{self.data_header.m_cCBSysNo}~|~"
            f"{self.data_header.m_iOldCenterNo}~|~"
            f"{self.data_header.m_iOldWindowNo}~|~"
            f"{self.data_header.m_iOldChanNo}~|~"
            f"{self.data_header.m_cOldSysNo}~|~"
            f"{self.data_header.m_cPolFileNo}~|~"
            f"{self.data_header.m_iPolOffsetNo}~|~"
            f"{self.data_header.m_cMatNo}~|~"
            f"{self.data_header.m_iBatchDep}~|~"
        )
        
        # Add conditional fields
        if self.data_header.m_iErrCode == 0:
            output_str += f"{self.data_header.m_iCallSeq}~|~"
        else:
            output_str += "0~|~"
            
        if self.data_header.m_iMsgCode == 202:
            output_str += "0~|~"
        else:
            output_str += f"{self.data_header.m_iTerminalType}~|~"
        return output_str

    def translate_header_to_tuple(self) -> tuple[str, ...]:
        # Handle last_log_seq with conditional logic
        last_log_seq_val = self.data_header.m_iLastLogSeq if self.data_header.m_iLastLogSeq < 2147483647 else 2147483647
        
        # Build initial part with @|@ delimiter
        data = (0,self.data_header.m_iMsgCode)
        
        # Build main part with ~|~ delimiter
        data += (
            self.data_header.m_sSysName,
            self.data_header.m_iMsgOrderNo,
            self.data_header.m_sSellingDate,
            self.data_header.m_iMsgSize,
            self.data_header.m_iMsgCode,
            self.data_header.m_iErrCode,
            self.data_header.m_iTrapCode,
            self.data_header.m_iStaffNo,
            self.data_header.m_iLogTermNo,
            self.data_header.m_iAcctNo,
            self.data_header.m_iFileNo,
            self.data_header.m_iBlockNo,
            self.data_header.m_iOverflowNo,
            self.data_header.m_iOffsetUnit,
            self.data_header.m_iTranNo,
            self.data_header.m_sTime,
            last_log_seq_val,
            self.data_header.m_iMsnNo,
            self.data_header.m_iExtSysType,
            self.data_header.m_iCatchUp,
            self.data_header.m_iBtExcept,
            self.data_header.m_iOtherSys,
            self.data_header.m_iPreLog,
            self.data_header.m_iTimeout,
            self.data_header.m_iLateReply,
            self.data_header.m_iBcsMsg,
            self.data_header.m_iRcvMsg,
            self.data_header.m_iOverFlow,
            self.data_header.m_iEscRel,
            self.data_header.m_iNoFlush,
            self.data_header.m_iTrainAcct,
            self.data_header.m_iSessionInfo,
            self.data_header.m_iSourceType,
            self.data_header.m_cVoiceFENo,
            self.data_header.m_sTerminalNo,
            self.data_header.m_iVoiceLocId,
            self.data_header.m_iDidCitNo,
            self.data_header.m_cDidPseTermNo,
            self.data_header.m_cDidFENo,
            self.data_header.m_sDidCitType,
            self.data_header.m_iCBCenterNo,
            self.data_header.m_iCBWindowNo,
            self.data_header.m_iCBLogTermNo,
            self.data_header.m_cCBSysNo,
            self.data_header.m_iOldCenterNo,
            self.data_header.m_iOldWindowNo,
            self.data_header.m_iOldChanNo,
            self.data_header.m_cOldSysNo,
            self.data_header.m_cPolFileNo,
            self.data_header.m_iPolOffsetNo,
            self.data_header.m_cMatNo,
            self.data_header.m_iBatchDep,
        )
        
        # Add conditional fields
        if self.data_header.m_iErrCode == 0:
            data += (self.data_header.m_iCallSeq,)
        else:
            data += (0,)
            
        if self.data_header.m_iMsgCode == 202:
            data += (0,)
        else:
            data += (self.data_header.m_iTerminalType,)
        return data

    def packHeader(self):
        pMlog = self.m_pMlog
        pMsg = self.m_pMsg

        self.data_header.m_iSysNo = pMsg.m_iSysNo
        self.data_header.m_iMsgOrderNo = self.m_iLoggerMsgOrderNo
        self.data_header.m_sSysName = pMsg.m_iSysName
        self.data_header.m_sSellingDate = datetime(
            year = pMsg.m_iMsgYear,
            month = pMsg.m_iMsgMonth,
            day = pMsg.m_iMsgDay
        )
        self.data_header.m_iMsgSize = ctypes.c_uint(pMlog.hdr.sizew).value
        self.data_header.m_iMsgCode = ctypes.c_uint(pMlog.hdr.codewu).value
        self.data_header.m_iErrCode = ctypes.c_uint(pMsg.m_iMsgErrwu).value
        if self.data_header.m_iErrCode != 0:
            self.data_header.m_iErrCode = 1

        self.data_header.m_iTrapCode = ctypes.c_ubyte(pMlog.hdr.trapcodebu).value
        self.data_header.m_iStaffNo = ctypes.c_uint(pMlog.hdr.stafflu).value
        self.data_header.m_iLogTermNo = ctypes.c_uint(pMlog.hdr.ltnlu).value
        self.data_header.m_iAcctNo = ctypes.c_uint(pMlog.hdr.acclu).value
        self.data_header.m_iFileNo = ctypes.c_uint(pMlog.hdr.filebu).value
        self.data_header.m_iBlockNo = ctypes.c_uint(pMlog.hdr.blocklu).value
        self.data_header.m_iOverflowNo = ctypes.c_uint(pMlog.hdr.overflowlu).value
        self.data_header.m_iOffsetUnit = ctypes.c_uint(pMlog.hdr.offwu).value
        self.data_header.m_iTranNo = ctypes.c_uint(pMlog.hdr.tranwu).value
        self.data_header.m_iLastLogSeq = ctypes.c_uint(pMlog.hdr.lgslu).value
        self.data_header.m_iMsnNo = ctypes.c_uint(pMlog.hdr.msnlu).value
        self.data_header.m_iExtSysType = ctypes.c_ubyte(pMlog.hdr.extSysTypebu).value
        self.data_header.m_iCatchUp = ctypes.c_ushort(pMlog.hdr.catchup1).value
        self.data_header.m_iBtExcept = ctypes.c_ushort(pMlog.hdr.btexc1).value
        self.data_header.m_iOtherSys = ctypes.c_ushort(pMlog.hdr.othsys1).value
        self.data_header.m_iPreLog = ctypes.c_ushort(pMlog.hdr.prelog1).value
        self.data_header.m_iTimeout = ctypes.c_ushort(pMlog.hdr.timeout1).value
        self.data_header.m_iLateReply = ctypes.c_ushort(pMlog.hdr.laterpy1).value
        self.data_header.m_iBcsMsg = ctypes.c_ushort(pMlog.hdr.bcsmsg1).value
        self.data_header.m_iRcvMsg = ctypes.c_ushort(pMlog.hdr.rcvmsg1).value
        self.data_header.m_iOverFlow = ctypes.c_ushort(pMlog.hdr.overflow1).value
        self.data_header.m_iEscRel = ctypes.c_ushort(pMlog.hdr.escRel1).value
        self.data_header.m_iNoFlush = ctypes.c_ushort(pMlog.hdr.noFlush1).value
        self.data_header.m_iTrainAcct = ctypes.c_ushort(pMlog.hdr.train1).value
        self.data_header.m_iSessionInfo = ctypes.c_ushort(pMlog.hdr.sessionInfo1).value
        self.data_header.m_iSourceType = ctypes.c_ubyte(pMlog.hdr.source.srcTypebu).value
        self.data_header.m_sTime = datetime.fromtimestamp(pMsg.m_iMsgTime)
    
        # ABMsgTranslator.cpp: line 231
        def pid_to_asc(pidwu: int) -> str:
            """
            Convert a 16-bit PID to its ASCII representation.
            Mirrors ABMsgTranslator::pidToAsc logic.
            """
            first_char = 0
            second_char = 0
            final_position = 0

            if pidwu != 0:
                first_char = pidwu // 2600
                second_char = ((pidwu - first_char * 2600) // 100) + 65
                final_position = (pidwu - first_char * 2600) - ((second_char - 65) * 100)

            return f"{first_char}{chr(second_char)}{final_position:02d}"


        # Values are kepy default in else, so no need to set them
        if self.data_header.m_iSourceType == LOGAB_SRC_VOICE:
            self.data_header.m_cVoiceFENo = ctypes.c_ubyte(pMlog.hdr.source.data.voice.febu).value
            self.data_header.m_iVoiceTermNo = ctypes.c_ushort(pMlog.hdr.source.data.voice.termwu).value
            self.data_header.m_iVoiceLocId = ctypes.c_uint(pMlog.hdr.source.data.voice.locidlu).value

            if self.data_header.m_iVoiceTermNo >= 30000:
                self.data_header.m_sTerminalNo = f"TBAS{(self.data_header.m_iVoiceTermNo - 30000):4}"
            else:
                self.data_header.m_sTerminalNo = pid_to_asc(self.data_header.m_iVoiceTermNo)
        

        # ABMsgTranslator.cpp: line 253
        cit_type_map = {
                0: "MPB",     1: "CIT-3",   2: "CIT-3A",  3: "CIT-5",   4: "CIT-6",
                5: "TWM",     6: "CIT-PDA", 7: "ESC",     8: "EWIN",    9: "CIT-8",
                10: "JCBW",   11: "AMBS",   12: "WLPDA",  13: "IP-PHONE",14: "ITV",
                15: "WLPDA",  16: "JCBWEKBA",17: "ITV",   18: "APINOW", 19: "IOSBS",
                20: "JCMOW",  21: "IBT",    22: "AOSBS",  23: "APISMC", 24: "APITD",
                25: "IBUT",   26: "APIWC",  27: "IBUA",   28: "WOSBS",  29: "MASBAI",
                30: "MASBAA", 99: "ECBPCC"
            }

        # Values are kepy default in else, so no need to set them
        if self.data_header.m_iSourceType in (LOGAB_SRC_CIT, LOGAB_SRC_EFT_CIT, LOGAB_SRC_EWIN, LOGAB_SRC_EFT_EWIN):
            # CIT
            # Meraged EWIN cause the logic is the same
            self.data_header.m_iDidCitNo    = pMlog.hdr.source.data.did.citlu
            self.data_header.m_cDidPseTermNo = pMlog.hdr.source.data.did.termbu
            self.data_header.m_cDidFENo     = pMlog.hdr.source.data.did.febu       
            idx = ctypes.c_ubyte(pMlog.hdr.source.data.did.citTypebu).value - 1
            self.data_header.m_sDidCitType = cit_type_map.get(idx, "")

        # ABMsgTranslator.cpp: line 297
        # ESC / CB_BT / EFT_CB / OLD / CB_EWAL
        if self.data_header.m_iSourceType in (LOGAB_SRC_CB_BT, LOGAB_SRC_EFT_CB, LOGAB_SRC_OLD, LOGAB_SRC_CB_EWAL):
            self.data_header.m_iCBCenterNo  = pMlog.hdr.source.data.cbBt.centrelu
            self.data_header.m_iCBWindowNo  = pMlog.hdr.source.data.cbBt.windowwu
            self.data_header.m_iCBLogTermNo = pMlog.hdr.source.data.cbBt.ltnwu
            self.data_header.m_cCBSysNo     = pMlog.hdr.source.data.cbBt.cbbu

            self.data_header.m_iOldCenterNo = pMlog.hdr.source.data.old.centrelu
            self.data_header.m_iOldWindowNo = pMlog.hdr.source.data.old.windowwu
            self.data_header.m_iOldChanNo   = pMlog.hdr.source.data.old.chanwu
            self.data_header.m_cOldSysNo    = pMlog.hdr.source.data.old.cbbu

        # EWIN / EFT_EWIN with IBT logic
        elif self.data_header.m_iSourceType in (LOGAB_SRC_EWIN, LOGAB_SRC_EFT_EWIN):
            if pMlog.hdr.source.data.did.citTypebu == DEV_TYP_IBT:
                # Separate IBT number for anonymous account
                self.data_header.m_iCBCenterNo  = self.data_header.m_iDidCitNo // 100000
                self.data_header.m_iCBWindowNo  = 0
                self.data_header.m_iCBLogTermNo = 0
        # Values 
        #  m_iCBCenterNo, m_iCBWindowNo, m_iCBLogTermNo, m_cCBSysNo,
        #  m_iOldCenterNo, m_iOldWindowNo, m_iOldChanNo, m_cOldSysNo 
        # are kepy default in else, so no need to set them

        # All other sources
        # Values are kepy default in else, so no need to set them
        if self.data_header.m_iSourceType == LOGAB_SRC_POL:
            self.data_header.m_cPolFileNo    = pMlog.hdr.source.data.pol.filebu
            self.data_header.m_iPolOffsetNo  = pMlog.hdr.source.data.pol.offsetlu

        # ABMsgTranslator.cpp: line 349
        # Values are kepy default in else, so no need to set them
        if self.data_header.m_iSourceType == LOGAB_SRC_MAT:
            self.data_header.m_iMatNo = pMlog.hdr.source.data.matlu
            # format as uppercase hexadecimal without the "0x" prefix
            self.data_header.m_cMatNo = format(self.data_header.m_iMatNo, 'X')

        if self.data_header.m_iSourceType == LOGAB_SRC_BAT_DEP:
            self.data_header.m_iBatchDep = pMlog.hdr.source.data.tbwu

        # ABMsgTranslator.cpp: line 429
        self.data_header.m_iCallSeq = ctypes.c_longlong(pMlog.hdr.custSessIdd).value

        # ABMsgTranslator.cpp: line 364
        self.data_header.m_iTerminalType = self.get_terminal_type()

        # Customer session ID
        self.data_header.m_iCallSeq = pMlog.hdr.custSessIdd
        
        # Calculate total amount based on message code
        iTotalAmt = 0
        m_iBetType = 0

        if self.data_header.m_iMsgCode == LOGAB_CODE_LOT:
            iTotalAmt = pMlog.data.bt.lot.tran.bet.d.hdr.costlu
            m_iBetType = pMlog.data.bt.lot.tran.bet.d.hdr.bettypebu
        elif self.data_header.m_iMsgCode == LOGAB_CODE_RAC:
            iTotalAmt = pMlog.data.bt.rac.tran.bet.d.hdr.costlu
            m_iBetType = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu
        elif self.data_header.m_iMsgCode == LOGAB_CODE_SB:
            iTotalAmt = pMlog.data.bt.sb.bet.tran.bet.hdr.costlu
            m_iBetType = pMlog.data.bt.sb.bet.tran.bet.hdr.bettypebu
        elif self.data_header.m_iMsgCode == LOGAB_CODE_DEP:
            iTotalAmt = pMlog.data.bt.dep.tran.amountdu
        elif self.data_header.m_iMsgCode == LOGAB_CODE_BATDEP:
            iTotalAmt = pMlog.data.deph.data.tran.data.amtdu
        elif self.data_header.m_iMsgCode == LOGAB_CODE_EFT_MISC:
            # iTotalAmt = pMlog.data.bt.eftmisc.eps.
            pass
        else:
            iTotalAmt = 0
