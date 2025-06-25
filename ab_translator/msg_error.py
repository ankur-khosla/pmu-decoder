from datetime import datetime
import ctypes

from ab_translator.ab_translator import ABTranslator
from ab_translator.msg import Msg
from ab_translator.data_structures import LOGAB
from ab_translator.constants import *


class MsgError():
    def __init__(self, pMlog: LOGAB, pMsg: Msg):
        self.m_pMlog = pMlog
        self.m_pMsg = pMsg
        self.m_iLoggerMsgOrderNo = 0
        self.m_iMsgOrderNo = 0
        self.m_iTerminalType = 0
        self.m_iBetType = 0
        self.iTotalAmt = 0

        self._getError()

    # ABMsgTranslator.cpp: line 231
    def pid_to_asc(self, pidwu: int) -> str:
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
    
    # Not tested yet

    def has_error(self) -> bool:
        pMlog = self.m_pMlog
        pMsg = self.m_pMsg
        has_message_error = (pMsg.m_iMsgErrwu != 0) and (pMlog.hdr.codewu != LOGAB_CODE_ACA)
        has_header_error = (pMlog.hdr.prelog1 != 0 or 
                            pMlog.hdr.laterpy1 != 0 or 
                            pMlog.hdr.timeout1 != 0 or
                            pMlog.hdr.train1 != 0)
        return has_message_error or has_header_error

    # Not tested yet
    def _getError(self) -> tuple[bool, str]:
        pMlog = self.m_pMlog
        pMsg = self.m_pMsg

        self.m_iCallSeq = pMlog.hdr.custSessIdd
        self.m_iSysNo = pMsg.m_iSysNo
        self.m_iMsgOrderNo = self.m_iLoggerMsgOrderNo

        self.m_sSysName = pMsg.m_iSysName

        self.m_sSellingDate = datetime(
            year = pMsg.m_iMsgYear,
            month = pMsg.m_iMsgMonth,
            day = pMsg.m_iMsgDay
        )

        self.m_iMsgSize = pMlog.hdr.sizew
        self.m_iMsgCode = pMlog.hdr.codewu
        self.m_iErrCode = pMsg.m_iMsgErrwu
        self.m_iTrapCode = pMlog.hdr.trapcodebu
        self.m_iStaffNo = pMlog.hdr.stafflu
        self.m_iLogTermNo = pMlog.hdr.ltnlu
        self.m_iAcctNo = pMlog.hdr.acclu
        self.m_iFileNo = pMlog.hdr.filebu
        self.m_iBlockNo = pMlog.hdr.blocklu
        self.m_iOverflowNo = pMlog.hdr.overflowlu
        self.m_iOffsetUnit = pMlog.hdr.offwu
        self.m_iTranNo = pMlog.hdr.tranwu
        self.m_iLastLogSeq = ctypes.c_uint(pMlog.hdr.lgslu).value
        self.m_iMsnNo = pMlog.hdr.msnlu
        self.m_iExtSysType = pMlog.hdr.extSysTypebu
        self.m_iCatchUp = pMlog.hdr.catchup1
        self.m_iBtExcept = pMlog.hdr.btexc1
        self.m_iOtherSys = pMlog.hdr.othsys1
        self.m_iPreLog = pMlog.hdr.prelog1
        self.m_iTimeout = pMlog.hdr.timeout1
        self.m_iLateReply = pMlog.hdr.laterpy1
        self.m_iBcsMsg = pMlog.hdr.bcsmsg1
        self.m_iRcvMsg = pMlog.hdr.rcvmsg1
        self.m_iOverFlow = pMlog.hdr.overflow1
        self.m_iEscRel = pMlog.hdr.escRel1
        self.m_iNoFlush = pMlog.hdr.noFlush1
        self.m_iTrainAcct = pMlog.hdr.train1
        self.m_iSessionInfo = pMlog.hdr.sessionInfo1
        self.m_iSourceType = pMlog.hdr.source.srcTypebu
        self.m_sTime = datetime.fromtimestamp(pMsg.m_iMsgTime)
        
        # Voice handling
        if self.m_iSourceType == LOGAB_SRC_VOICE:
            self.m_cVoiceFENo = pMlog.hdr.source.data.voice.febu
            self.m_iVoiceTermNo = pMlog.hdr.source.data.voice.termwu
            self.m_iVoiceLocId = pMlog.hdr.source.data.voice.locidlu

            self.m_sTerminalNo = f"{self.m_iVoiceTermNo:04X}"
            if not (self.m_sTerminalNo[0] == 'B' and self.m_sTerminalNo[1] == 'A'):
                self.m_sTerminalNo = self.pid_to_asc(self.m_iVoiceTermNo)
            else:
                if len(self.m_sTerminalNo) > 9:
                    self.m_sTerminalNo = self.m_sTerminalNo[:9]
        else:
            self.m_cVoiceFENo = 0
            self.m_iVoiceTermNo = 0
            self.m_iVoiceLocId = 0
            self.m_sTerminalNo = ""
        
        # CIT device types
        m_cCitType = {
            0: "MPB", 1: "CIT-3", 2: "CIT-3A", 3: "CIT-5", 4: "CIT-6", 5: "TWM", 
            6: "CIT-PDA", 7: "ESC", 8: "EWIN", 9: "CIT-8", 10: "JCBW", 11: "AMBS", 
            12: "WLPDA", 13: "IP-PHONE", 14: "ITV", 15: "WLPDA", 16: "JCBWEKBA", 
            17: "ITV", 18: "APINOW", 19: "IOSBS", 20: "JCMOW", 21: "IBT", 22: "AOSBS", 
            23: "APISMC", 24: "APITD", 25: "IBUT", 26: "APIWC", 27: "IBUA", 28: "WOSBS", 
            29: "MASBAI", 30: "MASBAA", 99: "ECBPCC"
        }

         # CIT and EWIN handling
        if (self.m_iSourceType == LOGAB_SRC_CIT) or (self.m_iSourceType == LOGAB_SRC_EFT_CIT):
            self.m_iDidCitNo = pMlog.hdr.source.data.did.citlu
            self.m_cDidPseTermNo = pMlog.hdr.source.data.did.termbu
            self.m_cDidFENo = pMlog.hdr.source.data.did.febu
            self.m_sDidCitType = m_cCitType.get(pMlog.hdr.source.data.did.citTypebu - 1, "")

        elif (self.m_iSourceType == LOGAB_SRC_EWIN) or (self.m_iSourceType == LOGAB_SRC_EFT_EWIN):
            self.m_iDidCitNo = pMlog.hdr.source.data.did.citlu
            self.m_cDidPseTermNo = pMlog.hdr.source.data.did.termbu
            self.m_cDidFENo = pMlog.hdr.source.data.did.febu
            
            citTypebu = pMlog.hdr.source.data.did.citTypebu
            if citTypebu == DEV_TYP_INET:
                self.m_sDidCitType = "EWIN"
            elif citTypebu == DEV_TYP_JCBW:
                self.m_sDidCitType = "JCBW"
            elif citTypebu == DEV_TYP_JCBWEKBA:
                self.m_sDidCitType = "JCBWEKBA"
            elif citTypebu == DEV_TYP_AMBS:
                self.m_sDidCitType = "AMBS"
            elif citTypebu == DEV_TYP_WLPDA:
                self.m_sDidCitType = "WLPDA"
            elif citTypebu == DEV_TYP_IPPHONE:
                self.m_sDidCitType = "IP-PHONE"
            elif citTypebu == DEV_TYP_MBSN:
                self.m_sDidCitType = "APINOW"
            elif citTypebu == DEV_TYP_IOSBS:
                self.m_sDidCitType = "IOSBS"
            elif citTypebu == DEV_TYP_JCMOW:
                self.m_sDidCitType = "JCMOW"
            elif citTypebu == DEV_TYP_IBT:
                self.m_sDidCitType = "IBT"
            elif citTypebu == DEV_TYP_AOSBS:
                self.m_sDidCitType = "AOSBS"
            elif citTypebu == DEV_TYP_APISMC:
                self.m_sDidCitType = "APISMC"
            elif citTypebu == DEV_TYP_APITD:
                self.m_sDidCitType = "APITD"
            elif citTypebu == DEV_TYP_IBUT:
                self.m_sDidCitType = "IBUT"
            elif citTypebu == DEV_TYP_IBUA:
                self.m_sDidCitType = "IBUA"
            elif citTypebu == DEV_TYP_API3HK:
                self.m_sDidCitType = "APIWC"
            elif citTypebu == DEV_TYP_WOSBS:
                self.m_sDidCitType = "WOSBS"
            elif citTypebu == DEV_TYP_MASBAI:
                self.m_sDidCitType = "MASBAI"
            elif citTypebu == DEV_TYP_MASBAA:
                self.m_sDidCitType = "MASBAA"
            else:
                self.m_sDidCitType = "UDF"
        else:
            self.m_iDidCitNo = 0
            self.m_cDidPseTermNo = 0
            self.m_cDidFENo = 0
            self.m_sDidCitType = ""

        # Initialize CB values
        self.m_iCBCenterNo = 0
        self.m_iCBWindowNo = 0
        self.m_iCBLogTermNo = 0
        self.m_cCBSysNo = 0
        self.m_iOldCenterNo = 0
        self.m_iOldWindowNo = 0
        self.m_iOldChanNo = 0
        self.m_cOldSysNo = 0

                # ESC/CB handling
        if ((self.m_iSourceType == LOGAB_SRC_CB_BT) or 
            (self.m_iSourceType == LOGAB_SRC_EFT_CB) or
            (self.m_iSourceType == LOGAB_SRC_CB_EWAL)):
            
            self.m_iCBCenterNo = pMlog.hdr.source.data.cbBt.centrelu
            self.m_iCBWindowNo = pMlog.hdr.source.data.cbBt.windowwu
            self.m_iCBLogTermNo = pMlog.hdr.source.data.cbBt.ltnwu
            self.m_cCBSysNo = pMlog.hdr.source.data.cbBt.cbbu

            self.m_iOldCenterNo = pMlog.hdr.source.data.old.centrelu
            self.m_iOldWindowNo = pMlog.hdr.source.data.old.windowwu
            self.m_iOldChanNo = pMlog.hdr.source.data.old.chanwu
            self.m_cOldSysNo = pMlog.hdr.source.data.old.cbbu
            
        elif (self.m_iSourceType == LOGAB_SRC_EWIN) or (self.m_iSourceType == LOGAB_SRC_EFT_EWIN):
            # 2011IBT - Separate IBT Number into Location, Table and Terminal for Anonymous Account Only
            if pMlog.hdr.source.data.did.citTypebu == DEV_TYP_IBT:
                self.m_iCBCenterNo = self.m_iDidCitNo // 100000
                self.m_iCBWindowNo = 0
                self.m_iCBLogTermNo = 0

        # POL data
        self.m_cPolFileNo = pMlog.hdr.source.data.pol.filebu
        self.m_iPolOffsetNo = pMlog.hdr.source.data.pol.offsetlu

        # MAT handling
        if self.m_iSourceType == LOGAB_SRC_MAT:
            self.m_iMatNo = pMlog.hdr.source.data.matlu
            self.m_cMatNo = f"{self.m_iMatNo:X}"
        else:
            self.m_iMatNo = 0
            self.m_cMatNo = ""

        # Batch deposit
        if self.m_iSourceType == LOGAB_SRC_BAT_DEP:
            self.m_iBatchDep = pMlog.hdr.source.data.tbwu
        else:
            self.m_iBatchDep = 0

        self.iTotalAmt = 0
        self.m_iBetType = 0

        if self.m_iMsgCode == LOGAB_CODE_LOT:
            self.iTotalAmt = pMlog.data.bt.lot.tran.bet.d.hdr.costlu
            self.m_iBetType = pMlog.data.bt.lot.tran.bet.d.hdr.bettypebu
        elif self.m_iMsgCode == LOGAB_CODE_RAC:
            self.iTotalAmt = pMlog.data.bt.rac.tran.bet.d.hdr.costlu
            self.m_iBetType = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu
        elif self.m_iMsgCode == LOGAB_CODE_SB:
            self.iTotalAmt = pMlog.data.bt.sb.bet.tran.bet.hdr.costlu
            self.m_iBetType = pMlog.data.bt.sb.bet.tran.bet.hdr.bettypebu
        elif self.m_iMsgCode == LOGAB_CODE_DEP:
            self.iTotalAmt = pMlog.data.bt.dep.tran.amountdu
        elif self.m_iMsgCode == LOGAB_CODE_BATDEP:
            self.iTotalAmt = pMlog.data.deph.data.tran.data.amtdu
        elif self.m_iMsgCode == LOGAB_CODE_EFT_MISC:
            # self.iTotalAmt = pMlog.data.bt.eftmisc.eps
            pass

    def get_error_to_string(self) -> str:
        last_log_seq_val = self.m_iLastLogSeq if self.m_iLastLogSeq < 2147483647 else 2147483647
        iPolOffsetNo = self.m_iPolOffsetNo if self.m_iPolOffsetNo < 2147483647 else 2147483647

        outputStr = (
            f"0@|@"
            f"{LOGAB_CODE_ERR}@|@"
            f"{self.m_sSysName}~|~"
            f"{self.m_iMsgOrderNo}~|~"
            f"{self.m_sSellingDate.strftime("%d-%b-%Y")}~|~"
            f"{self.m_iMsgSize}~|~"
            f"{self.m_iMsgCode}~|~"
            f"{self.m_iErrCode}~|~"
            f"{self.m_iTrapCode}~|~"
            f"{self.m_iStaffNo}~|~"
            f"{self.m_iLogTermNo}~|~"
            f"{self.m_iAcctNo}~|~"
            f"{self.m_iFileNo}~|~"
            f"{self.m_iBlockNo}~|~"
            f"{self.m_iOverflowNo}~|~"
            f"{self.m_iOffsetUnit}~|~"
            f"{self.m_iTranNo}~|~"
            f"{self.m_sTime.strftime("%d-%b-%Y %H:%M:%S")}~|~"
            f"{last_log_seq_val}~|~"
            f"{self.m_iMsnNo}~|~"
            f"{self.m_iExtSysType}~|~"
            f"{self.m_iCatchUp}~|~"
            f"{self.m_iBtExcept}~|~"
            f"{self.m_iOtherSys}~|~"
            f"{self.m_iPreLog}~|~"
            f"{self.m_iTimeout}~|~"
            f"{self.m_iLateReply}~|~"
            f"{self.m_iBcsMsg}~|~"
            f"{self.m_iRcvMsg}~|~"
            f"{self.m_iOverFlow}~|~"
            f"{self.m_iEscRel}~|~"
            f"{self.m_iNoFlush}~|~"
            f"{self.m_iTrainAcct}~|~"
            f"{self.m_iSessionInfo}~|~"
            f"{self.m_iSourceType}~|~"
            f"{self.m_cVoiceFENo}~|~"
            f"{self.m_sTerminalNo}~|~"
            f"{self.m_iVoiceLocId}~|~"
            f"{self.m_iDidCitNo}~|~"
            f"{self.m_cDidPseTermNo}~|~"
            f"{self.m_cDidFENo}~|~"
            f"{self.m_sDidCitType}~|~"
            f"{self.m_iCBCenterNo}~|~"
            f"{self.m_iCBWindowNo}~|~"
            f"{self.m_iCBLogTermNo}~|~"
            f"{self.m_cCBSysNo}~|~"
            f"{self.m_iOldCenterNo}~|~"
            f"{self.m_iOldWindowNo}~|~"
            f"{self.m_iOldChanNo}~|~"
            f"{self.m_cOldSysNo}~|~"
            f"{self.m_cPolFileNo}~|~"
            f"{iPolOffsetNo}~|~"
            f"{self.m_cMatNo}~|~"
            f"{self.m_iBatchDep}~|~"
            f"{self.m_iCallSeq}~|~"
            f"{self.m_iTerminalType}~|~"
            f"{self.m_iBetType}~|~"
            f"{self.iTotalAmt}"
        )
        return outputStr

    def get_error_to_tuple(self) -> tuple[str, ...]:
        last_log_seq_val = self.m_iLastLogSeq if self.m_iLastLogSeq < 2147483647 else 2147483647
        iPolOffsetNo = self.m_iPolOffsetNo if self.m_iPolOffsetNo < 2147483647 else 2147483647

        data = (
            0,
            LOGAB_CODE_ERR,
            self.m_sSysName,
            self.m_iMsgOrderNo,
            self.m_sSellingDate,
            self.m_iMsgSize,
            self.m_iMsgCode,
            self.m_iErrCode,
            self.m_iTrapCode,
            self.m_iStaffNo,
            self.m_iLogTermNo,
            self.m_iAcctNo,
            self.m_iFileNo,
            self.m_iBlockNo,
            self.m_iOverflowNo,
            self.m_iOffsetUnit,
            self.m_iTranNo,
            self.m_sTime,
            last_log_seq_val,
            self.m_iMsnNo,
            self.m_iExtSysType,
            self.m_iCatchUp,
            self.m_iBtExcept,
            self.m_iOtherSys,
            self.m_iPreLog,
            self.m_iTimeout,
            self.m_iLateReply,
            self.m_iBcsMsg,
            self.m_iRcvMsg,
            self.m_iOverFlow,
            self.m_iEscRel,
            self.m_iNoFlush,
            self.m_iTrainAcct,
            self.m_iSessionInfo,
            self.m_iSourceType,
            self.m_cVoiceFENo,
            self.m_sTerminalNo,
            self.m_iVoiceLocId,
            self.m_iDidCitNo,
            self.m_cDidPseTermNo,
            self.m_cDidFENo,
            self.m_sDidCitType,
            self.m_iCBCenterNo,
            self.m_iCBWindowNo,
            self.m_iCBLogTermNo,
            self.m_cCBSysNo,
            self.m_iOldCenterNo,
            self.m_iOldWindowNo,
            self.m_iOldChanNo,
            self.m_cOldSysNo,
            self.m_cPolFileNo,
            iPolOffsetNo,
            self.m_cMatNo,
            self.m_iBatchDep,
            self.m_iCallSeq,
            self.m_iTerminalType,
            self.m_iBetType,
            self.iTotalAmt,
        )
        return data
        