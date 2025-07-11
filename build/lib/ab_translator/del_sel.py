from ab_translator.constants import *
from ab_translator.data_structures import LOGAB

class DelSel:
    @staticmethod
    def get_sel(pMlog: LOGAB, m_cType: int) -> str:
        # char legs[5], sels[1024]
        legs = ""
        sels = ""
        indexbu = 0

        if m_cType == BETTYP_AWP:
            indexbu = pMlog.data.bt.rac.tran.bet.d.var.a.fmlbu
            legs = DelSel.get_form(indexbu)
            sels = DelSel.fmt_aup(pMlog)
            return sels.strip()

        elif m_cType in (BETTYP_MK6, BETTYP_PWB):
            # Not implemented in C++ code
            return ""

        elif m_cType in (
            BETTYP_WINPLA, BETTYP_WIN, BETTYP_PLA, BETTYP_QIN, BETTYP_QPL,
            BETTYP_DBL, BETTYP_TCE, BETTYP_FCT, BETTYP_QTT, BETTYP_DQN,
            BETTYP_TBL, BETTYP_TTR, BETTYP_6UP, BETTYP_DTR, BETTYP_TRIO,
            BETTYP_QINQPL, BETTYP_FF, BETTYP_BWA, BETTYP_CWA,
            BETTYP_CWB, BETTYP_CWC, BETTYP_IWN
        ):
            sels = DelSel.fmt_nrm(pMlog)
            return sels.strip()

        else:
            return ""
        
    @staticmethod
    def get_form(index: int) -> str:
        formula_list = [
            "2x1", "2x3", 
            "3x1", "3x3", "3x4", "3x6", "3x7",
            "4x1", "4x4", "4x5", "4x6", "4x10", "4x11", "4x14", "4x15",
            "5x1", "5x5", "5x6", "5x10", "5x15", "5x16", "5x20", "5x25", "5x26", "5x30", "5x31",
            "6x1", "6x6", "6x7", "6x15", "6x20", "6x21", "6x22", "6x35", "6x41", "6x42", "6x50", "6x56", "6x57", "6x62", "6x63"
        ]
        return formula_list[index] if 0 <= index < len(formula_list) else ""
    
    @staticmethod
    def fmt_aup(pMlog) -> str:
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

                sels = DelSel.fmt_sln(pMlog, 0, True, a, sels)
                sels += DelSel.fmt_ind(pMlog, True, a)
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

                sels += DelSel.fmt_qin(pMlog, numofbnkbmp, 2, 0, True, a)
                sels += DelSel.fmt_ind(pMlog, True, a)
                sels += "/"

            elif bettype == BETTYP_FCT:
                if a == 0:
                    sels += f"{race_no}*"
                else:
                    sels += f"{race_no}*"

                sels += DelSel.fmt_ext_aup(pMlog, 2, a)
                sels += DelSel.fmt_ind(pMlog, True, a)
                sels += "/"
        return sels[:-1]
    
    @staticmethod
    def fmt_sln(pMlog: LOGAB, bmppos: int, allupt: bool, idwu: int, str_input: str) -> str:
        sels = str_input
        fldwu = RDS_MAXFLD
        iwu = 0

        if not allupt:
            bitmap = pMlog.data.bt.rac.tran.bet.d.var.es.sellu[bmppos]
            for jwu in range(1, fldwu + 1):
                if bitmap & (1 << jwu):
                    iwu += 1
                    sels += f"{jwu:02d}+"
        else:
            bitmap = pMlog.data.bt.rac.tran.bet.d.var.a.sel[idwu].sellu[bmppos]
            for jwu in range(1, fldwu + 1):
                if bitmap & (1 << jwu):
                    iwu += 1
                    sels += f"{jwu}+"

        # remove exactly one trailing '+' under the same C++ conditions
        hdr = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu
        leg = pMlog.data.bt.rac.tran.bet.d.var.a.sel[idwu].bettypebu

        if (hdr not in (BETTYP_TCE, BETTYP_QTT)
            and ((not allupt and hdr != BETTYP_FCT)
                or (allupt and leg != BETTYP_FCT))):
            sels = sels[:-1]
        return sels
    
    @staticmethod
    def fmt_ind(pMlog: LOGAB, allupt: bool, idwu: int) -> str:
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
    
    @staticmethod
    def fmt_qin2(pMlog: LOGAB, numofbnk: int, numofbmp: int, bmpposwu: int, allupt: bool, idwu: int) -> str:
        result = ""

        if numofbnk == 0:
            result = DelSel.fmt_sln2(pMlog, bmpposwu, False, 0, result)
        else:
            for iwu in range(numofbmp):
                part = DelSel.fmt_sln2(pMlog, iwu + bmpposwu, False, 0, "")
                if iwu > 0:
                    result += ">"
                result += part

        return result
    
    @staticmethod
    def fmt_sln2(pMlog: LOGAB, bmppos: int, allupt: bool, idwu: int, input_str: str) -> str:
        max_field = RDS_MAXFLD
        sels = input_str
        bitmap = pMlog.data.bt.rac.tran.bet.d.var.es.betexbnk.sellu[bmppos]

        for jwu in range(1, max_field + 1):
            if (bitmap & (1 << jwu)) != 0:
                sels += f"{jwu:02d}"
                sels += '+'

        return sels[:-1]
    
    @staticmethod
    def fmt_ext(pMlog, numofbmp: int, numofbnk: int) -> str:
        sels = ""
        ind = pMlog.data.bt.rac.tran.bet.d.var.es.ind
        sellu = pMlog.data.bt.rac.tran.bet.d.var.es.sellu

        # single/single banker TCE/QTT/FCT bet
        if ind.bnk1 == 0 and ind.fld1 == 0 and ind.mbk1 == 0 and ind.mul1 == 0:
            for i in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, i, False, 0, sels)
            return sels[:-1]

        # multi-banker bet
        if (ind.mbk1 & 0x01) == 1:
            for i in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, i, False, 0, sels)
                sels = sels[:-1] + '>'
            return sels[:-1]

        # multiple bet (non-banker)
        if (ind.mul1 & 0x01) == 1 and (ind.bnk1 & 0x01) == 0:
            for i in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, i, False, 0, sels)
            return sels[:-1]

        # single/multiple banker
        if (ind.bnk1 & 0x01) == 1:
            numofbnkbmp = 0
            for i in range(numofbmp):
                if sellu[i] == 0:
                    break
                numofbnkbmp += 1

            for i in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, i, False, 0, sels)
                if i == numofbnkbmp - 2:
                    sels = sels[:-1] + '>'
            return sels[:-1]

        return sels
    
    @staticmethod
    def fmt_qin(pMlog: LOGAB, numofbnk: int, numofbmp: int, bmpposwu: int, allupt: bool, idwu: int) -> str:
        sels = ""

        bettype = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu

        if not allupt:
            if numofbnk == 0:
                sels = DelSel.fmt_sln(pMlog, bmpposwu, False, 0, sels)
            else:
                for iwu in range(numofbmp):
                    sels = DelSel.fmt_sln(pMlog, iwu + bmpposwu, False, 0, sels)
                    if iwu < numofbmp - 1:
                        sep = '#' if bettype == BETTYP_IWN else '>'
                        sels += sep
        else:
            if numofbnk == 0:
                sels = DelSel.fmt_sln(pMlog, bmpposwu, True, idwu, sels)
            else:
                for iwu in range(numofbmp):
                    sels = DelSel.fmt_sln(pMlog, iwu + bmpposwu, True, idwu, sels)
                    if iwu < numofbmp - 1:
                        sels += '>'

        return sels
    
    @staticmethod
    def fmt_ext_aup(pMlog, numofbmp: int, idwu: int) -> str:
        sels = ""
        sel = pMlog.data.bt.rac.tran.bet.d.var.a.sel[idwu]
        numofbnkbmp = 0

        # Case: Single/single banker TCE/QTT/FCT
        if sel.ind.bnk1 == 0 and sel.ind.fld1 == 0 and sel.ind.mbk1 == 0 and sel.ind.mul1 == 0:
            for iwu in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, iwu, True, idwu, sels)
            return sels.rstrip('+')

        # Case: Multi-banker
        elif sel.ind.mbk1 & 0x01 == 1:
            for iwu in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, iwu, True, idwu, sels)
                sels = sels.rstrip('+') + '>'
            return sels.rstrip('>')

        # Case: Multi-bet with no banker
        elif (sel.ind.mul1 & 0x01 == 1) and (sel.ind.bnk1 & 0x01 == 0):
            for iwu in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, iwu, True, idwu, sels)
            return sels.rstrip('+')

        # Case: Single or multiple banker
        if sel.ind.bnk1 & 0x01:
            for iwu in range(numofbmp):
                if sel.sellu[iwu] == 0:
                    break
                numofbnkbmp += 1

            for iwu in range(numofbmp):
                sels = DelSel.fmt_sln(pMlog, iwu, True, idwu, sels)
                if iwu == numofbnkbmp - 2:
                    sels = sels.rstrip('+') + '>'
            return sels.rstrip('>')
        return sels
    
    @staticmethod
    def fmt_nrm(pMlog: LOGAB) -> str:
        sels = ""
        race_number = pMlog.data.bt.rac.tran.bet.d.var.es.racebu
        sels += f"{race_number}*"

        bettype = pMlog.data.bt.rac.tran.bet.d.hdr.bettypebu
        bnkbu = pMlog.data.bt.rac.tran.bet.d.var.es.betexbnk.bnkbu

        if bettype in [BETTYP_WINPLA, BETTYP_WIN, BETTYP_PLA, BETTYP_BWA, BETTYP_CWA, BETTYP_CWB, BETTYP_CWC]:
            sels = DelSel.fmt_sln(pMlog, 0, False, 0, sels)

        elif bettype in [BETTYP_QIN, BETTYP_QPL, BETTYP_TRIO, BETTYP_QINQPL, BETTYP_FF]:
            sels += DelSel.fmt_qin(pMlog, bnkbu[0], 2, 0, False, 0)

        elif bettype == BETTYP_IWN:
            sels += DelSel.fmt_qin(pMlog, 1, 2, 0, False, 0)

        elif bettype == BETTYP_TCE:
            sels += DelSel.fmt_ext(pMlog, 3, bnkbu[0])

        elif bettype == BETTYP_FCT:
            sels += DelSel.fmt_ext(pMlog, 2, bnkbu[0])

        elif bettype == BETTYP_QTT:
            sels += DelSel.fmt_ext(pMlog, 4, bnkbu[0])

        elif bettype in [BETTYP_DBL, BETTYP_TBL, BETTYP_6UP]:
            legwu = {BETTYP_DBL: 2, BETTYP_TBL: 3, BETTYP_6UP: 6}[bettype]
            for i in range(legwu):
                sels = DelSel.fmt_sln(pMlog, i, False, 0, sels)
                if i < legwu - 1:
                    sels += '/'

        elif bettype == BETTYP_TTR:
            legwu = 3
            for i in range(legwu):
                sels += DelSel.fmt_qin(pMlog, bnkbu[i], 2, i * 2, False, 0)
                if i < legwu - 1:
                    sels += '/'
            if pMlog.data.bt.rac.tran.bet.d.var.es.ind.twoentry:
                sels += f"|{race_number}*"
                for i in range(legwu):
                    sels += DelSel.fmt_qin2(pMlog, 0, 2, i * 2, False, 0)
                    if i < legwu - 1:
                        sels += '/'

        elif bettype in [BETTYP_DQN, BETTYP_DTR]:
            legwu = 2
            for i in range(legwu):
                sels += DelSel.fmt_qin(pMlog, bnkbu[i], 2, i * 2, False, 0)
                if i < legwu - 1:
                    sels += '/'

        # Append indicators
        sels += DelSel.fmt_ind(pMlog, False, 0)

        return sels