import Msg
import time
import ctypes
import math
from constants import *
from data_structures import LOGAB



class ABRace:
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
    
    def packHeader(self, cpStoreProcName: str, pMlog: LOGAB, pMsg: Msg) -> str:
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
            f"{self.m_iLastLogSeq}~|~"
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
            outputStr+=f"{self.m_iTerminalType}~|~"

        return outputStr


    def translate_action(self, pMsg: Msg, pMlog: LOGAB) -> str:
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
            self.m_sFormula = self.get_form(self.m_cFormula)

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

        m_cSelections = self.get_sel(pMlog, self.m_cBetType)
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

    def get_sel(self, pMlog: LOGAB, m_cType: int) -> str:
        # char legs[5], sels[1024]
        legs = ""
        sels = ""
        indexbu = 0

        if m_cType == BETTYP_AWP:
            indexbu = pMlog.data.bt.rac.tran.bet.d.var.a.fmlbu
            legs = self.get_form(indexbu)  # assumed to return string
            sels = self.fmt_aup(pMlog)     # assumed to return string
            return sels.strip()

        elif m_cType in (BETTYP_MK6, BETTYP_PWB):
            # Placeholder for future implementation:
            # sels = fmtMk6(pMlog, pMlog.d.bt.lot.tsn.s.w12.type3)
            # return osi_atrim(sels)
            return ""

        elif m_cType in (
            BETTYP_WINPLA, BETTYP_WIN, BETTYP_PLA, BETTYP_QIN, BETTYP_QPL,
            BETTYP_DBL, BETTYP_TCE, BETTYP_FCT, BETTYP_QTT, BETTYP_DQN,
            BETTYP_TBL, BETTYP_TTR, BETTYP_6UP, BETTYP_DTR, BETTYP_TRIO,
            BETTYP_QINQPL, BETTYP_FF, BETTYP_BWA, BETTYP_CWA,
            BETTYP_CWB, BETTYP_CWC, BETTYP_IWN
        ):
            sels = self.fmt_nrm(pMlog)  # assumed to return string
            return sels.strip()

        else:
            return ""
        
    def get_form(self, index: int) -> str:
        formula_list = [
            "2x1", "2x3", 
            "3x1", "3x3", "3x4", "3x6", "3x7",
            "4x1", "4x4", "4x5", "4x6", "4x10", "4x11", "4x14", "4x15",
            "5x1", "5x5", "5x6", "5x10", "5x15", "5x16", "5x20", "5x25", "5x26", "5x30", "5x31",
            "6x1", "6x6", "6x7", "6x15", "6x20", "6x21", "6x22", "6x35", "6x41", "6x42", "6x50", "6x56", "6x57", "6x62", "6x63"
        ]
        return formula_list[index] if 0 <= index < len(formula_list) else ""
    
    def fmt_aup(self, pMlog) -> str:
        sels = ""
        numofbnkbmp = 0
        selections = pMlog.data.bt.rac.tran.bet.d.var.a.sel
        event_count = pMlog.data.bt.rac.tran.bet.d.var.a.evtbu

        for a in range(event_count):
            sel = selections[a]
            race_no = sel.racebu
            bettype = sel.bettypebu

            if bettype in (
                BETTYP_WINPLA, BETTYP_WIN, BETTYP_PLA,
                BETTYP_BWA, BETTYP_CWA, BETTYP_CWB, BETTYP_CWC
            ):
                if a == 0:
                    sels += f"{race_no}*"
                else:
                    sels += f"{race_no}*"

                sels += self.fmt_sln(pMlog, 0, True, a)
                sels += self.fmt_ind(pMlog, True, a)
                sels += "/"

            elif bettype in (
                BETTYP_IWN, BETTYP_QIN, BETTYP_QPL, BETTYP_TRIO,
                BETTYP_QINQPL, BETTYP_FF
            ):
                if a == 0:
                    sels += f"{race_no}*"
                else:
                    sels += f"{race_no}*"

                if sel.ind.bnk1 & 0x01:
                    numofbnkbmp = 1

                sels += self.fmt_qin(pMlog, numofbnkbmp, 2, 0, True, a)
                sels += self.fmt_ind(pMlog, True, a)
                sels += "/"

            elif bettype == BETTYP_FCT:
                if a == 0:
                    sels += f"{race_no}*"
                else:
                    sels += f"{race_no}*"

                sels += self.fmt_ext_aup(pMlog, 2, a)
                sels += self.fmt_ind(pMlog, True, a)
                sels += "/"

            # else: ignore other bettypes

        return sels.rstrip("/")  # remove trailing slash
    
    def fmt_sln(self, pMlog: LOGAB, bmppos: int, allupt: bool, idwu: int) -> str:
        sels = ""
        fldwu = RDS_MAXFLD  # maximum number of selection fields

        if not allupt:  # standard/exotic bet
            bitmap = pMlog.data.bt.rac.tran.bet.d.var.es.sellu[bmppos]
            for jwu in range(1, fldwu + 1):
                if bitmap & (1 << jwu):
                    sels += f"{jwu:02d}+"
        else:  # allup bet
            bitmap = pMlog.data.bt.rac.tran.bet.d.var.a.sel[idwu].sellu[bmppos]
            for jwu in range(1, fldwu + 1):
                if bitmap & (1 << jwu):
                    sels += f"{jwu}+"

        # cancel last '+' unless it's TCE, QTT, or FCT under specific conditions
        bettype_hdr = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu
        bettype_leg = pMlog.data.bt.rac.tran.bet.d.var.a.sel[idwu].bettypebu

        if bettype_hdr not in (BETTYP_TCE, BETTYP_QTT) and (
            (not allupt and bettype_hdr != BETTYP_FCT) or
            (allupt and bettype_leg != BETTYP_FCT)
        ):
            sels = sels.rstrip('+')

        return sels
    
    def fmt_ind(self, pMlog: LOGAB, allupt: bool, idwu: int) -> str:
        result = ""

        if not allupt:
            fld_flag = pMlog.data.bt.rac.tran.bet.d.var.es.ind.fld1 & 0x01
            mul_flag = pMlog.data.bt.rac.tran.bet.d.var.es.ind.mul1 & 0x01

            if fld_flag:
                result += "F"
            if mul_flag:
                result += "M"
        else:
            sel = pMlog.data.bt.rac.tran.bet.d.var.a.sel[idwu].ind
            if sel.fld1 & 0x01:
                result += "F"
            if sel.mul1 & 0x01:
                result += "M"

        return result
    
    def fmt_qin2(self, pMlog: LOGAB, numofbnk: int, numofbmp: int, bmpposwu: int, allupt: bool, idwu: int) -> str:
        result = ""

        if numofbnk == 0:
            result += self.fmtSln2(pMlog, bmpposwu, False, 0)
        else:
            for iwu in range(numofbmp):
                part = self.fmtSln2(pMlog, iwu + bmpposwu, False, 0)
                if iwu > 0:
                    result += ">"
                result += part

        return result
    
    def fmt_sln2(self, pMlog: LOGAB, bmppos: int, allupt: bool, idwu: int) -> str:
        max_field = RDS_MAXFLD
        sels = []
        bitmap = pMlog.data.bt.rac.tran.bet.d.var.es.betexbnk.sellu[bmppos]

        for jwu in range(1, max_field + 1):
            if (bitmap & (1 << jwu)) != 0:
                sels.append(f"{jwu:02d}")

        return '+'.join(sels)
    
    def fmt_qin(self, pMlog: LOGAB, numofbnk: int, numofbmp: int, bmpposwu: int, allupt: bool, idwu: int) -> str:
        sels = []

        bettype = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu

        if not allupt:
            if numofbnk == 0:
                sels.append(self.fmt_sln(pMlog, bmpposwu, False, 0))
            else:
                for iwu in range(numofbmp):
                    sels.append(self.fmt_sln(pMlog, iwu + bmpposwu, False, 0))
                    if iwu < numofbmp - 1:
                        sep = '#' if bettype == BETTYP_IWN else '>'
                        sels.append(sep)
        else:
            if numofbnk == 0:
                sels.append(self.fmt_sln(pMlog, bmpposwu, True, idwu))
            else:
                for iwu in range(numofbmp):
                    sels.append(self.fmt_sln(pMlog, iwu + bmpposwu, True, idwu))
                    if iwu < numofbmp - 1:
                        sels.append('>')

        return ''.join(sels)
    
    def fmt_ext_aup(self, pMlog, numofbmp: int, idwu: int) -> str:
        sels = []
        sel = pMlog.data.bt.rac.tran.bet.d.var.a.sel[idwu]
        numofbnkbmp = 0

        # Helper to append fmtSln output
        def append_sln(iwu):
            return self.fmt_sln(pMlog, iwu, True, idwu)

        # Case: Single/single banker TCE/QTT/FCT
        if sel.ind.bnk1 == 0 and sel.ind.fld1 == 0 and sel.ind.mbk1 == 0 and sel.ind.mul1 == 0:
            for iwu in range(numofbmp):
                sels.append(append_sln(iwu))
            return ''.join(sels).rstrip('+')

        # Case: Multi-banker
        elif sel.ind.mbk1 & 0x01:
            for iwu in range(numofbmp):
                sels.append(append_sln(iwu))
                sels[-1] = sels[-1][:-1] + '>'  # Replace '+' with '>'
            return ''.join(sels).rstrip('>')

        # Case: Multi-bet with no banker
        elif sel.ind.mul1 & 0x01 and not (sel.ind.bnk1 & 0x01):
            for iwu in range(numofbmp):
                sels.append(append_sln(iwu))
            return ''.join(sels).rstrip('+')

        # Case: Single or multiple banker
        if sel.ind.bnk1 & 0x01:
            for iwu in range(numofbmp):
                if sel.sellu[iwu] == 0:
                    break
                numofbnkbmp += 1

            for iwu in range(numofbmp):
                sels.append(append_sln(iwu))
                if iwu == numofbnkbmp - 2:
                    sels[-1] = sels[-1][:-1] + '>'  # Replace '+' with '>'

            return ''.join(sels).rstrip('>')

        return ''.join(sels)
    
    def fmt_nrm(self, pMlog: LOGAB) -> str:
        sels = []
        race_number = pMlog.data.bt.rac.tran.bet.d.var.es.racebu
        sels.append(f"{race_number}*")

        bettype = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu
        bnkbu = pMlog.data.bt.rac.tran.bet.d.var.es.betexbnk.bnkbu

        if bettype in [BETTYP_WINPLA, BETTYP_WIN, BETTYP_PLA, BETTYP_BWA, BETTYP_CWA, BETTYP_CWB, BETTYP_CWC]:
            sels.append(self.fmt_sln(pMlog, 0, False, 0))

        elif bettype in [BETTYP_QIN, BETTYP_QPL, BETTYP_TRIO, BETTYP_QINQPL, BETTYP_FF]:
            sels.append(self.fmt_qin(pMlog, bnkbu[0], 2, 0, False, 0))

        elif bettype == BETTYP_IWN:
            sels.append(self.fmt_qin(pMlog, 1, 2, 0, False, 0))

        elif bettype == BETTYP_TCE:
            sels.append(self.fmt_ext(pMlog, 3, bnkbu[0]))

        elif bettype == BETTYP_FCT:
            sels.append(self.fmt_ext(pMlog, 2, bnkbu[0]))

        elif bettype == BETTYP_QTT:
            sels.append(self.fmt_ext(pMlog, 4, bnkbu[0]))

        elif bettype in [BETTYP_DBL, BETTYP_TBL, BETTYP_6UP]:
            legwu = {BETTYP_DBL: 2, BETTYP_TBL: 3, BETTYP_6UP: 6}[bettype]
            for i in range(legwu):
                sels.append(self.fmt_sln(pMlog, i, False, 0))
                if i < legwu - 1:
                    sels.append('/')

        elif bettype == BETTYP_TTR:
            legwu = 3
            for i in range(legwu):
                sels.append(self.fmt_qin(pMlog, bnkbu[i], 2, i * 2, False, 0))
                if i < legwu - 1:
                    sels.append('/')
            if pMlog.data.bt.rac.tran.bet.d.var.es.ind.twoentry:
                sels.append(f"|{race_number}*")
                for i in range(legwu):
                    sels.append(self.fmt_qin2(pMlog, 0, 2, i * 2, False, 0))
                    if i < legwu - 1:
                        sels.append('/')

        elif bettype in [BETTYP_DQN, BETTYP_DTR]:
            legwu = 2
            for i in range(legwu):
                sels.append(self.fmt_qin(pMlog, bnkbu[i], 2, i * 2, False, 0))
                if i < legwu - 1:
                    sels.append('/')

        # Append indicators
        sels.append(self.fmt_ind(pMlog, False, 0))

        return ''.join(sels)