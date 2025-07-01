from datetime import datetime, date
from ctypes import addressof, cast, POINTER
from zoneinfo import ZoneInfo

from ab_translator.constants import *
from ab_translator.ab_translator import ABTranslator
from ab_translator.msg import Msg
from ab_translator.data_structures import LOGAB, BETLOTVAR


class ABCancelTranslator(ABTranslator):
    def __init__(self, pMlog: LOGAB, pMsg: Msg):
        super().__init__(pMlog, pMsg)
        self._load_data()
    
    def _load_data(self) -> str:
        pMlog = self.m_pMlog
        pMsg = self.m_pMsg
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

        self.m_sTranDate = datetime.fromtimestamp(pMlog.data.bt.can.businessDate, tz=ZoneInfo("Asia/Hong_Kong"))

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

            # struct BETLOTVAR *pLOTVAR;
            # union BETLOTN *pLTON;
            # pLTON = (union BETLOTN *)&pMlog->data.bt.can.data.lot.tran.bet.d.var.lot.n.sel;
            pLTON = addressof(pMlog.data.bt.can.data.lot.tran.bet.d.var.lot.n.sel)

            if self.m_cMultiEntriesFlag == 0:
                # BETLOTN 61
                # BETLOTM 61
                # BETLOTS 25
                # pLOTVAR = (struct BETLOTVAR *) ((char *) pLTON + 25);
                pLOTVAR_ptr = cast(pLTON + 25, POINTER(BETLOTVAR))
                pLOTVAR = pLOTVAR_ptr.contents

                if self.m_iLMultiDraw == 1:
                    # m_iNoOfDrawSelected = pLOTVAR->md.drselbu;
                    # m_iNoOfDrawRemain = pLOTVAR->md.drrembu;
                    self.m_iNoOfDrawSelected = pLOTVAR.md.drselbu
                    self.m_iNoOfDrawRemain = pLOTVAR.md.drrembu
                else:
                    self.m_iNoOfDrawSelected = 1
                    self.m_iNoOfDrawRemain = 1
        
                self.m_iNoOfEntries = 0  # Not used in single entry path

            else:
                # m_iNoOfEntries = pMlog->data.bt.can.data.lot.tran.bet.d.var.lot.n.sel.multi.entbu;
                m_iNoOfEntries = pMlog.data.bt.can.data.lot.tran.bet.d.var.lot.n.sel.multi.entbu

                if m_iNoOfEntries <= 4:
                    pLOTVAR_ptr = cast(pLTON + 1 + 4 * 6, POINTER(BETLOTVAR))
                else:
                    pLOTVAR_ptr = cast(pLTON + 1 + m_iNoOfEntries * 6, POINTER(BETLOTVAR))

                pLOTVAR = pLOTVAR_ptr.contents
                
                if self.m_iLMultiDraw == 1:
                    # m_iNoOfDrawSelected = pLOTVAR->md.drselbu;
                    # m_iNoOfDrawRemain = pLOTVAR->md.drrembu;
                    self.m_iNoOfDrawSelected = pLOTVAR.md.drselbu
                    self.m_iNoOfDrawRemain = pLOTVAR.md.drrembu
                else:
                    self.m_iNoOfDrawSelected = 1
                    self.m_iNoOfDrawRemain = 1

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
        self.m_sRMeetDate = ""

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
            md_str = ""
            if bet_type == BETTYP_AUP:
                md_str =       str(pMlog.data.bt.can.data.rac.tran.bet.d.var.a.md)
                self.m_cRLoc = pMlog.data.bt.rac.tran.bet.d.var.a.loc
                self.m_cRDay = pMlog.data.bt.rac.tran.bet.d.var.a.day
            else:
                md_str =       str(pMlog.data.bt.can.data.rac.tran.bet.d.var.es.md)
                self.m_cRLoc = pMlog.data.bt.can.data.rac.tran.bet.d.var.es.loc
                self.m_cRDay = pMlog.data.bt.can.data.rac.tran.bet.d.var.es.day

    
            if len(md_str) == 8:
                self.m_sRMeetDate = datetime.strptime(md_str, "%Y%m%d").replace(tzinfo=ZoneInfo("Asia/Hong_Kong"))
            else:
                self.m_sRMeetDate = ""

            self.m_cRType    = pMlog.data.bt.can.data.rac.tran.bet.d.hdr.bettypebu
            self.m_iRUnitBet = pMlog.data.bt.can.data.rac.tran.bet.d.hdr.betinvcomb.flexi.baseinv
            self.m_iRTtlCost = pMlog.data.bt.can.data.rac.tran.bet.d.hdr.costlu

        # Cancel Withdrawal
        if self.m_iCanCode == ACU_CODE_WTW:
            # wtw = pMlog.data.bt.can.data.wtw.tran
            self.m_iWAmount    = pMlog.data.bt.can.data.wtw.tran.amountd
            self.m_iWSvcCharge = pMlog.data.bt.can.data.wtw.tran.chargedu
            self.m_iWType      = pMlog.data.bt.can.data.wtw.tran.typebu
            self.m_cWActBy     = pMlog.data.bt.can.data.wtw.tran.actBybu
            self.m_cWSrcType   = pMlog.data.bt.can.data.wtw.tran.srcbu
            self.m_cWCanFlag   = pMlog.data.bt.can.data.wtw.tran.cancel1
        else:
            self.m_iWAmount = 0
            self.m_iWSvcCharge = 0
            self.m_iWType = 0
            self.m_cWActBy = 0
            self.m_cWSrcType = 0
            self.m_cWCanFlag = 0



        # Cancel SB
        if self.m_iCanCode in (ACU_CODE_SB, ACU_CODE_SB2):
            # sb = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr
            self.m_iSSrcSell = pMlog.data.bt.can.data.sb.bet.tran.srcbu
            self.m_iSUnitBet = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.betinvcomb.flexi.baseinv
            self.m_iSTtlCost = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.costlu
            self.m_sSSelltime = datetime.fromtimestamp(pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.sellTime, tz=ZoneInfo("Asia/Hong_Kong"))
            self.m_cSBetType = pMlog.data.bt.can.data.sb.bet.tran.bet.hdr.bettypebu
        else:
            self.m_iSSrcSell = 0
            self.m_iSUnitBet = 0
            self.m_iSTtlCost = 0
            self.m_cSBetType = 0
            self.m_sSSelltime = ""

        # Cancel Deposit
        if self.m_iCanCode in (ACU_CODE_DEP, ACU_CODE_DEP_TSN2):
            # dep = pMlog.data.bt.can.data.dep.tran
            self.m_sDHoldTime = datetime.fromtimestamp(pMlog.data.bt.can.data.dep.tran.holdtime, tz=ZoneInfo("Asia/Hong_Kong"))
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
    
    def translate_to_string(self) -> str:
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

        if isinstance(self.m_sRMeetDate, (datetime, date)):
            str_m_sRMeetDate = self.m_sRMeetDate.strftime("%Y-%m-%d 00:00:00")
        else:
            str_m_sRMeetDate = ""

        outputStr += (
            f"{self.m_iRMeetIndex}~|~"
            f"{self.m_cRErrRaceNo}~|~"
            f"{self.m_cRErrSel}~|~"
            f"{self.m_iROffset}~|~"
            f"{self.m_cRSrcSell}~|~"
            f"{str_m_sRMeetDate}~|~"
            f"{self.m_cRLoc}~|~"
            f"{self.m_cRDay}~|~"
            f"{self.m_cRType}~|~"
            f"{self.m_iRUnitBet}~|~"
            f"{self.m_iRTtlCost}~|~"
        )

        outputStr += (
            f"{self.m_iWAmount}~|~"
            f"{self.m_iWSvcCharge}~|~"
            f"{self.m_iWType}~|~"
            f"{self.m_cWActBy}~|~"
            f"{self.m_cWSrcType}~|~"
            f"{self.m_cWCanFlag}~|~"
        )

        if isinstance(self.m_sSSelltime, (datetime, date)):
            str_m_sSSelltime = self.m_sSSelltime.strftime("%d-%b-%Y")
        else:
            str_m_sSSelltime = ""

        outputStr += (
            f"{self.m_iSSrcSell}~|~"
            f"{self.m_iSUnitBet}~|~"
            f"{self.m_iSTtlCost}~|~"
            f"{str_m_sSSelltime}~|~"
            f"{self.m_cSBetType}~|~"
        )

        if isinstance(self.m_sDHoldTime, (datetime, date)):
            str_m_sDHoldTime = self.m_sDHoldTime.strftime("%d-%b-%Y")
        else:
            str_m_sDHoldTime = ""
        outputStr += (
            f"{str_m_sDHoldTime}~|~"
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
            f"{self.m_sTranDate.strftime("%-d-%b-%Y")}"
        )

        return self.translate_header_to_string() + outputStr
    
    def translate_to_tuple(self) -> tuple[str, ...]:

        data = (
            self.m_iTranNo,
            self.m_iCanCode,
            self.m_cFileNo,
            self.m_iBlkNo,
            self.m_cOffUnit,
            self.m_cOthUnit,
            self.m_cEarCall,
            self.m_cTsnFlag, 
        )

        data += (
            self.m_iLIndex,
            self.m_iLErrSel,
            self.m_iLOffset,
            self.m_cLSrcSell,
            self.m_iLDrawYr,
            self.m_iLDrawNo,
            self.m_iLDrawType,
            float(self.m_iLUnitBet),
            float(self.m_iLTtlCost),
        )

        data += (
            self.m_iRMeetIndex,
            self.m_cRErrRaceNo,
            self.m_cRErrSel,
            self.m_iROffset,
            self.m_cRSrcSell,
            self.m_sRMeetDate,
            self.m_cRLoc,
            self.m_cRDay,
            self.m_cRType,
            float(self.m_iRUnitBet),
            float(self.m_iRTtlCost),
        )

        data += (
            float(self.m_iWAmount),
            float(self.m_iWSvcCharge),
            self.m_iWType,
            self.m_cWActBy,
            self.m_cWSrcType,
            self.m_cWCanFlag,
        )

        data += (
            self.m_iSSrcSell,
            float(self.m_iSUnitBet),
            float(self.m_iSTtlCost),
            self.m_sSSelltime,
            self.m_cSBetType,
        )

        data += (
            self.m_sDHoldTime,
            float(self.m_iDAmount),
            float(self.m_iDSvcCharge),
            self.m_cDType,
            self.m_iDWithHoldFlag,
            self.m_iDCancelFlag,
            self.m_iDRevFlag,
            self.m_cDSrcDep,
            self.m_iLMultiDraw,
            self.m_iNoOfDrawSelected,
            self.m_iNoOfDrawRemain,
            self.m_cCanPrevDay,
            self.m_sTranDate,
        )

        return self.translate_header_to_tuple() + data