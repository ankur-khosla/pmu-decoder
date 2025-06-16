import time
import ctypes
import math
from ab_translator.constants import *
from ab_translator.data_structures import LOGAB
from ab_translator.del_sel import DelSel
from ab_translator.msg import Msg
from collections import defaultdict

class ABTranslator:
    def __init__(self):
        # Initialize all the fields that were in the C++ code

        # system identifiers
        self.m_iSysNo = 0
        self.m_iMsgOrderNo = 0
        self.m_sSellingDate = ""
        self.m_sSysName = ""

        # self.m_pTBAccount: Optional[TBAccount] = None

        self.m_iMsgSize = 0
        self.m_iMsgCode = 0
        self.m_iErrCode = 0
        self.m_iTrapCode = 0
        self.m_iStaffNo = 0
        
        self.m_iLogTermNo = 0
        self.m_iAcctNo = 0
        self.m_iFileNo = 0
        self.m_iBlockNo = 0
        self.m_iOverflowNo = 0
        self.m_iOffsetUnit = 0
        self.m_iTranNo = 0
        self.m_iLastLogSeq = 0
        self.m_iMsnNo = 0

        self.m_iExtSysType = 0
        self.m_iCatchUp = 0

        self.m_iBtExcept = 0

        self.m_iOtherSys = 0
        self.m_iPreLog = 0
        self.m_iTimeout = 0
        self.m_iLateReply = 0

        self.m_iBcsMsg = 0
        self.m_iRcvMsg = 0
        self.m_iOverFlow = 0
        self.m_iEscRel = 0
        self.m_iNoFlush = 0

        self.m_iTrainAcct = 0
        self.m_iSourceType = 0
        self.m_sTime = ""

        self.m_iMatNo = 0
        self.m_iBatchDep = 0
        self.m_cMatNo = ""

        self.m_cVoiceFENo = 0
        self.m_iVoiceTermNo = 0
        self.m_iVoiceLocId = 0

        self.m_iDidCitNo = 0
        self.m_cDidPseTermNo = 0
        self.m_cDidFENo = 0
        self.m_sDidCitType = ""

        self.m_iCBCenterNo = 0
        self.m_iCBWindowNo = 0
        self.m_iCBLogTermNo = 0
        self.m_cCBSysNo = 0

        self.m_iOldCenterNo = 0
        self.m_iOldWindowNo = 0
        self.m_iOldChanNo = 0
        self.m_cOldSysNo = 0

        self.m_cPolFileNo = 0
        self.m_iPolOffsetNo = 0

        self.m_iCallSeq = 0
        self.m_iSessionInfo = 0
        
        self.m_iLoggerMsgOrderNo = 0
        self.m_sMonths = MONTHS

        # added after error: 
        self.m_sTerminalNo = 0
        self.m_iTerminalType = 0

        self.m_iBitmap: list[int] = [0] * 6

        self.m_cAllupPoolType: list[int] = [0] * 6
        self.m_iAllupRaceNo: list[int] = [0] * 6
        self.m_cAllupBankerFlag: list[int] = [0] * 6
        self.m_cAllupFieldFlag: list[int] = [0] * 6
        self.m_cAllupMultiFlag: list[int] = [0] * 6
        self.m_cAllupMultiBankerFlag: list[int] = [0] * 6
        self.m_cAllupRandomFlag: list[int] = [0] * 6
        self.m_iNoOfCombination: list[int] = [0] * 6
        self.m_iPayFactor: list[int] = [0] * 6
        self.m_iAllupBankerBitmap: list[int] = [0] * 6
        self.m_iAllupSelectBitmap: list[int] = [0] * 6

        self.terminal_type_matrix = defaultdict(lambda: defaultdict(int))

    def format_msg_time(self, msg_time: int) -> str:
        tm_time = time.localtime(msg_time)
        return (
            f"{tm_time.tm_mday:02d}-"
            f"{MONTHS[tm_time.tm_mon - 1]}-"
            f"{tm_time.tm_year} "
            f"{tm_time.tm_hour:02d}:"
            f"{tm_time.tm_min:02d}:"
            f"{tm_time.tm_sec:02d}"
        )
    
    def get_terminal_type(self, msg:Msg, pMlog: LOGAB):

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

    
    def packHeader(self, pMlog: LOGAB, pMsg: Msg) -> str:
        self.m_iSysNo = pMsg.m_iSysNo
        self.m_iMsgOrderNo = self.m_iLoggerMsgOrderNo
        self.m_sSysName = pMsg.m_iSysName
        
        # Format selling date
        self.m_sSellingDate = f"{pMsg.m_iMsgDay:02d}-{self.m_sMonths[pMsg.m_iMsgMonth-1]}-{pMsg.m_iMsgYear}"
        
        self.m_iMsgSize = ctypes.c_uint(pMlog.hdr.sizew).value
        self.m_iMsgCode = ctypes.c_uint(pMlog.hdr.codewu).value
        self.m_iErrCode = ctypes.c_uint(pMsg.m_iMsgErrwu).value
        if self.m_iErrCode != 0:
            self.m_iErrCode = 1
        self.m_iTrapCode = ctypes.c_ubyte(pMlog.hdr.trapcodebu).value
        self.m_iStaffNo = ctypes.c_uint(pMlog.hdr.stafflu).value
        self.m_iLogTermNo = ctypes.c_uint(pMlog.hdr.ltnlu).value
        self.m_iAcctNo = ctypes.c_uint(pMlog.hdr.acclu).value
        self.m_iFileNo = ctypes.c_uint(pMlog.hdr.filebu).value
        self.m_iBlockNo = ctypes.c_uint(pMlog.hdr.blocklu).value
        self.m_iOverflowNo = ctypes.c_uint(pMlog.hdr.overflowlu).value
        self.m_iOffsetUnit = ctypes.c_uint(pMlog.hdr.offwu).value
        self.m_iTranNo = ctypes.c_uint(pMlog.hdr.tranwu).value
        self.m_iLastLogSeq = ctypes.c_uint(pMlog.hdr.lgslu).value
        self.m_iMsnNo = ctypes.c_uint(pMlog.hdr.msnlu).value
        self.m_iExtSysType = ctypes.c_ubyte(pMlog.hdr.extSysTypebu).value
        self.m_iCatchUp = ctypes.c_ushort(pMlog.hdr.catchup1).value
        self.m_iBtExcept = ctypes.c_ushort(pMlog.hdr.btexc1).value
        self.m_iOtherSys = ctypes.c_ushort(pMlog.hdr.othsys1).value
        self.m_iPreLog = ctypes.c_ushort(pMlog.hdr.prelog1).value
        self.m_iTimeout = ctypes.c_ushort(pMlog.hdr.timeout1).value
        self.m_iLateReply = ctypes.c_ushort(pMlog.hdr.laterpy1).value
        self.m_iBcsMsg = ctypes.c_ushort(pMlog.hdr.bcsmsg1).value
        self.m_iRcvMsg = ctypes.c_ushort(pMlog.hdr.rcvmsg1).value
        self.m_iOverFlow = ctypes.c_ushort(pMlog.hdr.overflow1).value
        self.m_iEscRel = ctypes.c_ushort(pMlog.hdr.escRel1).value
        self.m_iNoFlush = ctypes.c_ushort(pMlog.hdr.noFlush1).value
        self.m_iTrainAcct = ctypes.c_ushort(pMlog.hdr.train1).value
        self.m_iSessionInfo = ctypes.c_ushort(pMlog.hdr.sessionInfo1).value
        self.m_iSourceType = ctypes.c_ubyte(pMlog.hdr.source.srcTypebu).value
        self.m_sTime = self.format_msg_time(pMsg.m_iMsgTime)
    
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


        if self.m_iSourceType == LOGAB_SRC_VOICE:
            self.m_cVoiceFENo = ctypes.c_ubyte(pMlog.hdr.source.data.voice.febu).value
            self.m_iVoiceTermNo = ctypes.c_ushort(pMlog.hdr.source.data.voice.termwu).value
            self.m_iVoiceLocId = ctypes.c_uint(pMlog.hdr.source.data.voice.locidlu).value

            if self.m_iVoiceTermNo >= 30000:
                self.m_sTerminalNo = f"TBAS{(self.m_iVoiceTermNo - 30000):4}"
            else:
                self.m_sTerminalNo = pid_to_asc(self.m_iVoiceTermNo)
        else:
            self.m_cVoiceFENo = 0
            self.m_iVoiceTermNo = 0
            self.m_iVoiceLocId = 0
            self.m_sTerminalNo = ""
        
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

        if self.m_iSourceType in (LOGAB_SRC_CIT, LOGAB_SRC_EFT_CIT, LOGAB_SRC_EWIN, LOGAB_SRC_EFT_EWIN):
            # CIT
            # Meraged EWIN cause the logic is the same
            self.m_iDidCitNo    = pMlog.hdr.source.data.did.citlu
            self.m_cDidPseTermNo = pMlog.hdr.source.data.did.termbu
            self.m_cDidFENo     = pMlog.hdr.source.data.did.febu       
            idx = ctypes.c_ubyte(pMlog.hdr.source.data.did.citTypebu).value - 1
            self.m_sDidCitType = cit_type_map.get(idx, "")
        else:
            # other sources
            self.m_iDidCitNo    = 0
            self.m_cDidPseTermNo = 0
            self.m_cDidFENo     = 0
            self.m_sDidCitType  = ""
        
        # ABMsgTranslator.cpp: line 297
        # ESC / CB_BT / EFT_CB / OLD / CB_EWAL
        if self.m_iSourceType in (LOGAB_SRC_CB_BT, LOGAB_SRC_EFT_CB, LOGAB_SRC_OLD, LOGAB_SRC_CB_EWAL):
            self.m_iCBCenterNo  = pMlog.hdr.source.data.cbBt.centrelu
            self.m_iCBWindowNo  = pMlog.hdr.source.data.cbBt.windowwu
            self.m_iCBLogTermNo = pMlog.hdr.source.data.cbBt.ltnwu
            self.m_cCBSysNo     = pMlog.hdr.source.data.cbBt.cbbu

            self.m_iOldCenterNo = pMlog.hdr.source.data.old.centrelu
            self.m_iOldWindowNo = pMlog.hdr.source.data.old.windowwu
            self.m_iOldChanNo   = pMlog.hdr.source.data.old.chanwu
            self.m_cOldSysNo    = pMlog.hdr.source.data.old.cbbu

        # EWIN / EFT_EWIN with IBT logic
        elif self.m_iSourceType in (LOGAB_SRC_EWIN, LOGAB_SRC_EFT_EWIN):
            if pMlog.hdr.source.data.did.citTypebu == DEV_TYP_IBT:
                # Separate IBT number for anonymous account
                self.m_iCBCenterNo  = self.m_iDidCitNo // 100000
                self.m_iCBWindowNo  = 0
                self.m_iCBLogTermNo = 0

        # All other sources
        else:
            self.m_iCBCenterNo  = 0
            self.m_iCBWindowNo  = 0
            self.m_iCBLogTermNo = 0
            self.m_cCBSysNo     = 0

            self.m_iOldCenterNo = 0
            self.m_iOldWindowNo = 0
            self.m_iOldChanNo   = 0
            self.m_cOldSysNo    = 0

        if self.m_iSourceType == LOGAB_SRC_POL:
            self.m_cPolFileNo    = pMlog.hdr.source.data.pol.filebu
            self.m_iPolOffsetNo  = pMlog.hdr.source.data.pol.offsetlu
        else:
            self.m_cPolFileNo    = 0
            self.m_iPolOffsetNo  = 0

        # ABMsgTranslator.cpp: line 349
        if self.m_iSourceType == LOGAB_SRC_MAT:
            self.m_iMatNo = pMlog.hdr.source.data.matlu
            # format as uppercase hexadecimal without the "0x" prefix
            self.m_cMatNo = format(self.m_iMatNo, 'X')
        else:
            self.m_iMatNo = 0
            self.m_cMatNo = ""

        if self.m_iSourceType == LOGAB_SRC_BAT_DEP:
            self.m_iBatchDep = pMlog.hdr.source.data.tbwu
        else:
            self.m_iBatchDep = 0        

        # ABMsgTranslator.cpp: line 429
        self.m_iCallSeq = ctypes.c_longlong(pMlog.hdr.custSessIdd).value

        # ABMsgTranslator.cpp: line 364
        outputStr = (
            f"{0}@|@"
            f"{self.m_iMsgCode}@|@"
            f"{self.m_sSysName}~|~"
            f"{self.m_iMsgOrderNo}~|~"
            f"{self.m_sSellingDate}~|~"
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
            f"{self.m_sTime}~|~"
            f"{self.m_iLastLogSeq if self.m_iLastLogSeq < 2147483647 else 2147483647}~|~"
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
            f"{self.m_iPolOffsetNo}~|~"
            f"{self.m_cMatNo}~|~"
            f"{self.m_iBatchDep}~|~"
        )
        if self.m_iErrCode == 0:
            outputStr += f"{self.m_iCallSeq}~|~"
        else:
            outputStr += "0~|~"

        if self.m_iMsgCode == 202:
            outputStr+=f"0~|~"
        else:
            self.m_iTerminalType = self.get_terminal_type(pMsg, pMlog)
            outputStr+=f"{self.m_iTerminalType}~|~"

        

        return outputStr


    def translate_abrace(self, pMsg: Msg, pMlog: LOGAB) -> str:
        self.m_itotalPay = pMlog.data.bt.rac.tran.bet.d.hdr.totdu
        self.m_iTotalCost = pMlog.data.bt.rac.tran.bet.d.hdr.costlu
        self.m_iFlexiBetFlag = pMlog.data.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.flexibet


        if self.m_iFlexiBetFlag == 0:
            self.m_iUnitBet = pMlog.data.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.baseinv
            self.m_iUnitBetTenK = self.m_iUnitBet * 10000
            self.m_iTotalNoOfCombinations = (self.m_iTotalCost // 100) // self.m_iUnitBet

        else:
            self.m_iTotalNoOfCombinations = pMlog.data.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.baseinv

            a1 = float(self.m_iTotalCost)
            a2 = float(self.m_iTotalNoOfCombinations)

            tmp = a1 * 1000.0 / a2        # e.g., 6666666.6666
            tmp1 = tmp / 10.0             # e.g., 666666.6666
            tmp2 = math.floor(tmp1 + 0.5) # round to nearest integer

            self.m_iUnitBetTenK = int(tmp2)

        self.m_sSellTime = self.format_msg_time(pMsg.m_iMsgSellTime)
        self.m_cBetType = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu
        self.m_sBetType = self.get_bet_type(self.m_cBetType)

        if self.m_cBetType == BETTYP_AUP:
            self.m_cNoOfEvt = pMlog.data.bt.rac.tran.bet.d.var.a.evtbu
            self.m_cFormula = pMlog.data.bt.rac.tran.bet.d.var.a.fmlbu

            md_val = pMlog.data.bt.rac.tran.bet.d.var.a.md
            md_str = f"{md_val:08d}"
            if len(md_str) == 8:
                self.m_sMeetDate = f"{md_str[:4]}-{md_str[4:6]}-{md_str[6:8]} 00:00:00"

            self.m_cLoc = pMlog.data.bt.rac.tran.bet.d.var.a.loc
            self.m_cDay = pMlog.data.bt.rac.tran.bet.d.var.a.day
            self.m_sFormula = DelSel.get_form(self.m_cFormula)

            for a in range(6):
                sel = pMlog.data.bt.rac.tran.bet.d.var.a.sel[a]
                self.m_cAllupPoolType[a] = sel.bettypebu
                self.m_iAllupRaceNo[a] = sel.racebu
                self.m_cAllupBankerFlag[a] = sel.ind.bnk1
                self.m_cAllupFieldFlag[a] = sel.ind.fld1
                self.m_cAllupMultiFlag[a] = sel.ind.mul1
                self.m_cAllupMultiBankerFlag[a] = sel.ind.mbk1
                self.m_cAllupRandomFlag[a] = sel.ind.rand1
                self.m_iNoOfCombination[a] = sel.comwu
                self.m_iPayFactor[a] = sel.pftrlu
                self.m_iAllupBankerBitmap[a] = sel.sellu[0]
                self.m_iAllupSelectBitmap[a] = sel.sellu[1]
        else:
            self.m_iRaceNo = pMlog.data.bt.rac.tran.bet.d.var.es.racebu
            self.m_cBankerFlag = pMlog.data.bt.rac.tran.bet.d.var.es.ind.bnk1
            self.m_cFieldFlag = pMlog.data.bt.rac.tran.bet.d.var.es.ind.fld1
            self.m_cMultiFlag = pMlog.data.bt.rac.tran.bet.d.var.es.ind.mul1
            self.m_cMultiBankerFlag = pMlog.data.bt.rac.tran.bet.d.var.es.ind.mbk1
            self.m_cRandomFlag = pMlog.data.bt.rac.tran.bet.d.var.es.ind.rand1

            for a in range(6):
                self.m_iBitmap[a] = pMlog.data.bt.rac.tran.bet.d.var.es.sellu[a]

            md_val = pMlog.data.bt.rac.tran.bet.d.var.es.md
            md_str = f"{md_val:08d}"
            if len(md_str) == 8:
                self.m_sMeetDate = f"{md_str[:4]}-{md_str[4:6]}-{md_str[6:8]} 00:00:00"

            self.m_cLoc = pMlog.data.bt.rac.tran.bet.d.var.es.loc
            self.m_cDay = pMlog.data.bt.rac.tran.bet.d.var.es.day

        self.m_iAnonymous = pMlog.hdr.anonymous1  # Anonymous Account (2011IBT)
        self.m_iCscCard = pMlog.data.bt.rac.tran.bet.csctrn  # Transaction with CSC (201108PSR)


        outputStr = (
            f"{self.m_sMeetDate}~|~"
            f"{self.m_cLoc}~|~"
            f"{self.m_cDay}~|~"
            f"{self.m_itotalPay}~|~"
            f"{self.m_iUnitBetTenK}~|~"
            f"{self.m_iTotalCost}~|~"
            f"{self.m_sSellTime}~|~"
            f"{self.m_sBetType}~|~"
            f" ~|~"
        )

        if self.m_cBetType == BETTYP_AUP:
            outputStr += f"{self.m_cNoOfEvt}~|~"
            outputStr += f"{self.m_sFormula}~|~"

            for a in range(self.m_cNoOfEvt):
                self.m_sAllupBettype = self.get_bet_type(self.m_cAllupPoolType[a])
                outputStr += (
                    f"{self.m_sAllupBettype}~|~"
                    f"{self.m_iAllupRaceNo[a]}~|~"
                    f"{self.m_cAllupBankerFlag[a]}~|~"
                    f"{self.m_cAllupFieldFlag[a]}~|~"
                    f"{self.m_cAllupMultiFlag[a]}~|~"
                    f"{self.m_cAllupMultiBankerFlag[a]}~|~"
                    f"{self.m_cAllupRandomFlag[a]}~|~"
                    f"{self.m_iNoOfCombination[a]}~|~"
                    f"{self.m_iPayFactor[a]}~|~"
                )

            for a in range(self.m_cNoOfEvt, 6):
                outputStr += "0~|~" * 9

            outputStr += "0~|~" * 6

        else:
            outputStr += "0~|~" * 2
            outputStr += "0~|~" * 9 * 6
            outputStr += (
                f"{self.m_iRaceNo}~|~"
                f"{self.m_cBankerFlag}~|~"
                f"{self.m_cFieldFlag}~|~"
                f"{self.m_cMultiFlag}~|~"
                f"{self.m_cMultiBankerFlag}~|~"
                f"{self.m_cRandomFlag}~|~"
            )

        m_cSelections = DelSel.get_sel(pMlog, self.m_cBetType)
        trun_sel = m_cSelections[:1000] if len(m_cSelections) > 1000 else m_cSelections
        outputStr += f"{trun_sel}~|~"

        if self.m_cBetType < BETTYP_AUP or self.m_cBetType >= BETTYP_FF:
            for i in range(3):
                m_iNoOfBankers = pMlog.data.bt.rac.tran.bet.d.var.es.betexbnk.bnkbu[i]
                outputStr += f"{m_iNoOfBankers}~|~"

            for i in range(6):
                value = pMlog.data.bt.rac.tran.bet.d.var.es.sellu[i]
                if value > 65535:
                    m_sBitmap = "0000"
                else:
                    m_sBitmap = f"{value:04X}"
                outputStr += f"{m_sBitmap}~|~"
        else:
            # Allup ticket
            outputStr += "0~|~" * 3

            for i in range(self.m_cNoOfEvt):
                part1 = pMlog.data.bt.rac.tran.bet.d.var.a.sel[i].sellu[0]
                part2 = pMlog.data.bt.rac.tran.bet.d.var.a.sel[i].sellu[1]

                s1 = "0000" if part1 > 65535 else f"{part1:04X}"
                s2 = "0000" if part2 > 65535 else f"{part2:04X}"

                m_sBitmap = s1 + s2
                outputStr += f"{m_sBitmap}~|~"

            for i in range(self.m_cNoOfEvt, 6):
                outputStr += "0000~|~"

        # Cross sell and additional fields
        m_iCrossSell = pMlog.data.bt.rac.crossSellFl
        outputStr += (
            f"{m_iCrossSell}~|~"
            f"{self.m_iFlexiBetFlag}~|~"
            f"{self.m_iTotalNoOfCombinations}~|~"
            f"{self.m_iAnonymous}~|~"
            f"{self.m_iCscCard}"
        )
        return outputStr

    def get_bet_type(self, bet_type: int) -> str:
        return {
            BETTYP_WINPLA: "W-P",
            BETTYP_WIN:    "WIN",
            BETTYP_PLA:    "PLA",
            BETTYP_QIN:    "QIN",
            BETTYP_QPL:    "QPL",
            BETTYP_DBL:    "DBL",
            BETTYP_TCE:    "TCE",
            BETTYP_FCT:    "FCT",
            BETTYP_QTT:    "QTT",
            BETTYP_DQN:    "D-Q",
            BETTYP_TBL:    "TBL",
            BETTYP_TTR:    "T-T",
            BETTYP_6UP:    "6UP",
            BETTYP_DTR:    "D-T",
            BETTYP_TRIO:   "TRI",
            BETTYP_QINQPL: "QQP",
            BETTYP_CV:     "CV",
            BETTYP_MK6:    "MK6",
            BETTYP_PWB:    "PWB",
            BETTYP_AWP:    "ALUP",
            BETTYP_FF:     "F-F",
            BETTYP_BWA:    "BWA",
            BETTYP_CWA:    "CWA",
            BETTYP_CWB:    "CWB",
            BETTYP_CWC:    "CWC",
            BETTYP_IWN:    "IWN",
        }.get(bet_type, "XXXX")


    def translate_abcancel(self, pMsg: Msg, pMlog: LOGAB) -> str:

        self.m_iErrorCode = pMsg.m_iMsgErrwu

        self.m_iTranNo = pMlog.data.bt.can.tranwu
        self.m_iCanCode = pMlog.data.bt.can.codewu
        self.m_cFileNo = pMlog.data.bt.can.filebu
        self.m_iBlkNo = pMlog.data.bt.can.blocklu
        self.m_cOffUnit = pMlog.data.bt.can.offwu
        self.m_cOthUnit = pMlog.data.bt.can.otherUnit1
        self.m_cEarCall = pMlog.data.bt.can.canprv1
        self.m_cTsnFlag = pMlog.data.bt.can.byTsn1
        self.m_cCanPrevDay = pMlog.data.bt.can.canPrevDay


        outputStr = (
            f"{self.m_iTranNo}~|~"
            f"{self.m_iCanCode}~|~"
            f"{self.m_cFileNo}~|~"
            f"{self.m_iBlkNo}~|~"
            f"{self.m_cOffUnit}~|~"
            f"{self.m_cOthUnit}~|~"
            f"{self.m_cEarCall}~|~"
            f"{self.m_cTsnFlag}~|~"
        )

        tm_date = time.localtime(pMlog.data.bt.can.businessDate)
        self.m_sTranDate = f"{tm_date.tm_mday}-{MONTHS[tm_date.tm_mon-1]}-{tm_date.tm_year}"

        # Cancel Lottery
        if self.m_iCanCode in (ACU_CODE_LOT, ACU_CODE_LOT2,
                                ACU_CODE_AB_LOT_MD, ACU_CODE_ESC_LOT_MD):
            
            self.m_iLIndex       = pMlog.data.bt.can.data.lot.indexwu
            self.m_iLErrSel      = pMlog.data.bt.can.data.lot.selwu
            self.m_iLOffset      = pMlog.data.bt.can.data.lot.offsetlu
            self.m_cLSrcSell     = pMlog.data.bt.can.data.lot.tran.bet.srcbu

            self.m_iLDrawYr      = pMlog.data.bt.can.data.lot.tran.bet.d.var.lot.yearwu
            self.m_iLDrawNo      = pMlog.data.bt.can.data.lot.tran.bet.d.var.lot.drawwu
            self.m_iLDrawType    = pMlog.data.bt.can.data.lot.tran.bet.d.var.lot.typewu

            self.m_iLUnitBet     = pMlog.data.bt.can.data.lot.tran.bet.d.hdr.betinvcomb.flexi.baseinv
            self.m_iLTtlCost     = pMlog.data.bt.can.data.lot.tran.bet.d.hdr.costlu
            self.m_iLMultiDraw   = pMlog.data.bt.can.data.lot.multidraw
            
            # Adjust draw year
            if self.m_iLDrawYr < 50:
                self.m_iLDrawYr += 2000
            else:
                self.m_iLDrawYr += 1900

            # Multi-entry flag
            self.m_cMultiEntriesFlag = pMlog.data.bt.can.data.lot.tran.bet.d.var.lot.n.multi1

            # Determine entries and draw counts
            sel_union = pMlog.data.bt.can.data.lot.tran.bet.d.var.n.sel
            if self.m_cMultiEntriesFlag == 0:
                lotvar = sel_union.get_lotvar(offset=25)
            else:
                count = pMlog.data.bt.can.data.lot.tran.bet.d.var.lot.n.sel.multi.entbu
                offset = 1 + min(count, 4) * 6
                lotvar = sel_union.get_lotvar(offset=offset)

            if self.m_iLMultiDraw == 1:
                self.m_iNoOfDrawSelected = lotvar.md.drselbu
                self.m_iNoOfDrawRemain   = lotvar.md.drrembu
            else:
                self.m_iNoOfDrawSelected = 1
                self.m_iNoOfDrawRemain   = 1
        else:
            self.m_iLIndex = 0
            self.m_iLErrSel = 0
            self.m_iLOffset = 0
            self.m_cLSrcSell = 0
            self.m_iLDrawYr = 0
            self.m_iLDrawNo = 0
            self.m_iLDrawType = 0
            self.m_iLUnitBet = 0
            self.m_iLTtlCost = 0
            self.m_iLMultiDraw = 0
            self.m_iNoOfDrawSelected = 0
            self.m_iNoOfDrawRemain = 0

        outputStr += (
            f"{self.m_iLIndex}~|~"
            f"{self.m_iLErrSel}~|~"
            f"{self.m_iLOffset}~|~"
            f"{self.m_cLSrcSell}~|~"
            f"{self.m_iLDrawYr}~|~"
            f"{self.m_iLDrawNo}~|~"
            f"{self.m_iLDrawType}~|~"
            f"{self.m_iLUnitBet}~|~"
            f"{self.m_iLTtlCost}~|~"
        )

        # Cancel Racing
        self.m_iRMeetIndex = 0
        self.m_cRErrRaceNo = 0
        self.m_cRErrSel    = 0
        self.m_iROffset    = 0
        self.m_cRSrcSell   = 0
        self.m_cRLoc       = 0
        self.m_cRDay       = 0
        self.m_cRType      = 0
        self.m_iRUnitBet   = 0
        self.m_iRTtlCost   = 0
        self.m_sRMeetDate = "01-Jan-1900"

        if self.m_iCanCode in (ACU_CODE_RAC, ACU_CODE_RAC2):
            
            # rac = pMlog.data.bt.can.data.rac
            if self.m_iErrorCode == 0:
                self.m_iROffset = pMlog.data.bt.can.data.rac.betinfo.raceinfo.offsetlu
            else:
                self.m_iRMeetIndex = pMlog.data.bt.can.data.rac.indexwu
                err = pMlog.data.bt.can.data.rac.betinfo.errorinfo
                self.m_cRErrRaceNo = err.racebu
                self.m_cRErrSel    = err.selbu

            self.m_cRSrcSell = pMlog.data.bt.can.data.rac.tran.bet.srcbu

            # bet = pMlog.data.bt.can.data.rac.tran.bet
            # hdr = pMlog.data.bt.can.data.rac.tran.bet.d.hdr
            bet_type = pMlog.data.bt.can.data.rac.tran.bet.d.hdr.bettypebu

            # Default meeting date
            md = ""
            if bet_type == BETTYP_AUP:
                md =       str(pMlog.data.bt.can.data.rac.tran.bet.d.var.a.md)
                self.m_cRLoc = pMlog.data.bt.rac.tran.bet.d.var.a.loc
                self.m_cRDay = pMlog.data.bt.rac.tran.bet.d.var.a.day
            else:
                md =       str(pMlog.data.bt.can.data.rac.tran.bet.d.var.es.md)
                self.m_cRLoc = pMlog.data.bt.can.data.rac.tran.bet.d.var.es.loc
                self.m_cRDay = pMlog.data.bt.can.data.rac.tran.bet.d.var.es.day

            if len(md) == 8:
                yy, mm, dd = md[:4], md[4:6], md[6:8]
                self.m_sRMeetDate = f"{yy}-{mm}-{dd} 00:00:00"

            self.m_cRType    = pMlog.data.bt.can.data.rac.tran.bet.d.hdr.bettypebu
            self.m_iRUnitBet = pMlog.data.bt.can.data.rac.tran.bet.d.hdr.betinvcomb.flexi.baseinv
            self.m_iRTtlCost = pMlog.data.bt.can.data.rac.tran.bet.d.hdr.costlu

        outputStr += (
            f"{self.m_iRMeetIndex}~|~"
            f"{self.m_cRErrRaceNo}~|~"
            f"{self.m_cRErrSel}~|~"
            f"{self.m_iROffset}~|~"
            f"{self.m_cRSrcSell}~|~"
            f"{self.m_sRMeetDate}~|~"
            f"{self.m_cRLoc}~|~"
            f"{self.m_cRDay}~|~"
            f"{self.m_cRType}~|~"
            f"{self.m_iRUnitBet}~|~"
            f"{self.m_iRTtlCost}~|~"
        )

        # Cancel Withdrawal
        if self.m_iCanCode == ACU_CODE_WTW:
            # wtw = pMlog.data.bt.can.data.wtw.tran
            self.m_iWAmount    = pMlog.data.bt.can.data.wtw.amountd
            self.m_iWSvcCharge = pMlog.data.bt.can.data.wtw.chargedu
            self.m_iWType      = pMlog.data.bt.can.data.wtw.typebu
            self.m_cWActBy     = pMlog.data.bt.can.data.wtw.tran
            self.m_cWSrcType   = pMlog.data.bt.can.data.wtw.tran
            self.m_cWCanFlag   = pMlog.data.bt.can.data.wtw.tran
        else:
            self.m_iWAmount = 0
            self.m_iWSvcCharge = 0
            self.m_iWType = 0
            self.m_cWActBy = 0
            self.m_cWSrcType = 0
            self.m_cWCanFlag = 0

        outputStr += (
            f"{self.m_iWAmount}~|~"
            f"{self.m_iWSvcCharge}~|~"
            f"{self.m_iWType}~|~"
            f"{self.m_cWActBy}~|~"
            f"{self.m_cWSrcType}~|~"
            f"{self.m_cWCanFlag}~|~"
        )

        # Cancel SB
        if self.m_iCanCode in (ACU_CODE_SB, ACU_CODE_SB2):
            # sb = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr
            self.m_iSSrcSell = pMlog.data.bt.can.data.sb.bet.tran.srcbu
            self.m_iSUnitBet = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.betinvcomb.flexi.baseinv
            self.m_iSTtlCost = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.costlu

            s_time = time.localtime(pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.sellTime)
            self.m_sSSelltime = f"{s_time.tm_mday}-" + \
                                 f"{MONTHS[s_time.tm_mon-1]}-{1900 + s_time.tm_year}" if s_time else ""
            self.m_cSBetType = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.bettypebu
        else:
            self.m_iSSrcSell = 0
            self.m_iSUnitBet = 0
            self.m_iSTtlCost = 0
            self.m_cSBetType = 0
            self.m_sSSelltime = ""
            
        outputStr += (
            f"{self.m_iSSrcSell}~|~"
            f"{self.m_iSUnitBet}~|~"
            f"{self.m_iSTtlCost}~|~"
            f"{self.m_sSSelltime}~|~"
            f"{self.m_cSBetType}~|~"
        )

        # Cancel Deposit
        if self.m_iCanCode in (ACU_CODE_DEP, ACU_CODE_DEP_TSN2):
            # dep = pMlog.data.bt.can.data.dep.tran
            h_time = time.localtime(pMlog.data.bt.can.data.dep.tran.holdtime)
            self.m_sDHoldTime = f"{h_time.tm_mday}-{MONTHS[h_time.tm_mon-1]}-{1900 + h_time.tm_year}"
            self.m_iDAmount       = pMlog.data.bt.can.data.dep.tran.amountdu
            self.m_iDSvcCharge    = pMlog.data.bt.can.data.dep.tran.chargedu
            self.m_cDType         = pMlog.data.bt.can.data.dep.tran.typebu
            self.m_iDWithHoldFlag = pMlog.data.bt.can.data.dep.tran.hold1
            self.m_iDCancelFlag   = pMlog.data.bt.can.data.dep.tran.cancel1
            self.m_iDRevFlag      = pMlog.data.bt.can.data.dep.tran.reversed1
            self.m_cDSrcDep       = pMlog.data.bt.can.data.dep.tran.srcbu
        else:
            self.m_sDHoldTime = ""
            self.m_iDAmount = 0
            self.m_iDSvcCharge = 0
            self.m_cDType = 0
            self.m_iDWithHoldFlag = 0
            self.m_iDCancelFlag = 0
            self.m_iDRevFlag = 0
            self.m_cDSrcDep = 0

        outputStr += (
            f"{self.m_sDHoldTime}~|~"
            f"{self.m_iDAmount}~|~"
            f"{self.m_iDSvcCharge}~|~"
            f"{self.m_cDType}~|~"
            f"{self.m_iDWithHoldFlag}~|~"
            f"{self.m_iDCancelFlag}~|~"
            f"{self.m_iDRevFlag}~|~"
            f"{self.m_cDSrcDep}~|~"
            f"{self.m_iLMultiDraw}~|~"
            f"{self.m_iNoOfDrawSelected}~|~"
            f"{self.m_iNoOfDrawRemain}~|~"
            f"{self.m_cCanPrevDay}~|~"
            f"{self.m_sTranDate}"
        )
        return outputStr