import math
from ctypes import POINTER, cast, pointer, c_ubyte, c_ulonglong

from ab_translator.constants import *
from ab_translator.ab_translator import ABTranslator
from ab_translator.data_structures import LOGAB, BETAUPSEL
from ab_translator.del_sel import DelSel
from ab_translator.msg import Msg


class ABRaceTranslator(ABTranslator):
    def __init__(self, pMlog: LOGAB, pMsg: Msg):
        super().__init__(pMlog, pMsg)
        # Allup specific fields
        # self.data_allup = AllupSelectionData()
        self.m_iBitmap: list[int] = [0] * 6
        self.m_cAllupPoolType: list[int] = [0] * 6
        self.m_iAllupBankerBitmap: list[int] = [0] * 6
        self.m_iAllupSelectBitmap: list[int] = [0] * 6 
        self.m_sAllupBettype: str = ""
        self.m_iAllupRaceNo: list[int] = [0] * 6
        self.m_cAllupBankerFlag: list[int] = [0] * 6
        self.m_cAllupFieldFlag: list[int] = [0] * 6
        self.m_cAllupMultiFlag: list[int] = [0] * 6
        self.m_cAllupMultiBankerFlag: list[int] = [0] * 6
        self.m_cAllupRandomFlag: list[int] = [0] * 6
        self.m_iNoOfCombination: list[int] = [0] * 6
        self.m_iPayFactor: list[int] = [0] * 6

        self._load_data()

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
      
    def _load_data(self) -> str:
        pMlog = self.m_pMlog
        pMsg = self.m_pMsg
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

        m_cSelections = DelSel.get_sel(pMlog, self.m_cBetType)
        self.m_trun_sel = m_cSelections[:1000] if len(m_cSelections) > 1000 else m_cSelections

        if self.m_cBetType < BETTYP_AUP or self.m_cBetType >= BETTYP_FF:
            self.m_migrated_betexbnk_bnkbu = [c_ubyte(0).value] * 3
            self.m_migrated_betexbnk_sellu = [c_ulonglong(0).value] * 6
            
            for i in range(3):
                self.m_migrated_betexbnk_bnkbu[i] = pMlog.data.bt.rac.tran.bet.d.var.es.betexbnk.bnkbu[i]
            for i in range(6):
                self.m_migrated_betexbnk_sellu[i] = pMlog.data.bt.rac.tran.bet.d.var.es.sellu[i]
        else:
            # Allup ticket
            self.m_migrated_betaupsel = cast(pointer(pMlog.data.bt.rac.tran.bet.d.var.a.sel), POINTER(BETAUPSEL))

        # Cross sell and additional fields
        self.m_iCrossSell = pMlog.data.bt.rac.crossSellFl


    def translate_to_string(self) -> str:
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

        outputStr += f"{self.m_trun_sel}~|~"        

        if self.m_cBetType < BETTYP_AUP or self.m_cBetType >= BETTYP_FF:
            for i in range(3):
                outputStr += f"{self.m_migrated_betexbnk_bnkbu[i]}~|~"

            for i in range(6):
                if self.m_migrated_betexbnk_sellu[i] > 65535:
                    m_sBitmap = "0000"
                else:
                    m_sBitmap = f"{self.m_migrated_betexbnk_sellu[i]:04X}"
                outputStr += f"{m_sBitmap}~|~"
        else:
            # Allup ticket
            outputStr += "0~|~" * 3
            for i in range(self.m_cNoOfEvt):
                part1 = self.m_migrated_betaupsel[i].sellu[0]
                part2 = self.m_migrated_betaupsel[i].sellu[1]

                s1 = "0000" if part1 > 65535 else f"{part1:04X}"
                s2 = "0000" if part2 > 65535 else f"{part2:04X}"

                m_sBitmap = s1 + s2
                outputStr += f"{m_sBitmap}~|~"

            for i in range(self.m_cNoOfEvt, 6):
                outputStr += "0000~|~"

        outputStr += (
            f"{self.m_iCrossSell}~|~"
            f"{self.m_iFlexiBetFlag}~|~"
            f"{self.m_iTotalNoOfCombinations}~|~"
            f"{self.m_iAnonymous}~|~"
            f"{self.m_iCscCard}"
        )
        return self.translate_header_to_string() + outputStr
    
    def translate_to_tuple(self) -> tuple[str, ...]:

        data = (
            self.m_sMeetDate,
            str(self.m_cLoc),
            str(self.m_cDay),
            float(self.m_itotalPay),
            self.m_iUnitBetTenK,
            float(self.m_iTotalCost),
            self.m_sSellTime,
            self.m_sBetType, 
            " "
        )

        if self.m_cBetType == BETTYP_AUP:
            data += (
                self.m_cNoOfEvt,
                str(self.m_sFormula),
            )

            for a in range(self.m_cNoOfEvt):
                self.m_sAllupBettype = self.get_bet_type(self.m_cAllupPoolType[a])
                data += (
                    str(self.m_sAllupBettype),
                    str(self.m_iAllupRaceNo[a]),
                    self.m_cAllupBankerFlag[a],
                    self.m_cAllupFieldFlag[a],
                    self.m_cAllupMultiFlag[a],
                    self.m_cAllupMultiBankerFlag[a],
                    self.m_cAllupRandomFlag[a],
                    self.m_iNoOfCombination[a],
                    float(self.m_iPayFactor[a]),
                )

            for a in range(self.m_cNoOfEvt, 6):
                data += (str(0), str(0), 0, 0, 0, 0, 0, 0, float(0))
            data += (str(0), 0, 0, 0, 0, 0)
        else:
            data += (0, str(0))
            for a in range(0, 6):
                data += (str(0), str(0), 0, 0, 0, 0, 0, 0, float(0))
            data += (
                str(self.m_iRaceNo),
                self.m_cBankerFlag,
                self.m_cFieldFlag,
                self.m_cMultiFlag,
                self.m_cMultiBankerFlag,
                self.m_cRandomFlag,
            )

        data += (self.m_trun_sel,)

        if self.m_cBetType < BETTYP_AUP or self.m_cBetType >= BETTYP_FF:
            for i in range(3):
                data += (self.m_migrated_betexbnk_bnkbu[i],)

            for i in range(6):
                if self.m_migrated_betexbnk_sellu[i] > 65535:
                    m_sBitmap = "0000"
                else:
                    m_sBitmap = f"{self.m_migrated_betexbnk_sellu[i]:04X}"
                data += (m_sBitmap,)
        else:
            # Allup ticket
            data += (0, 0, 0)
            for i in range(self.m_cNoOfEvt):
                part1 = self.m_migrated_betaupsel[i].sellu[0]
                part2 = self.m_migrated_betaupsel[i].sellu[1]

                s1 = "0000" if part1 > 65535 else f"{part1:04X}"
                s2 = "0000" if part2 > 65535 else f"{part2:04X}"

                m_sBitmap = s1 + s2
                data += (m_sBitmap,)

            for i in range(self.m_cNoOfEvt, 6):
                data += ("0000~|~",)

        data += (
            self.m_iCrossSell,
            self.m_iFlexiBetFlag,
            self.m_iTotalNoOfCombinations,
            self.m_iAnonymous,
            self.m_iCscCard
        )

        return self.translate_header_to_tuple() + data