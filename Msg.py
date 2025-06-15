class Msg:
    def __init__(self, msg_size: int = 8000):
        
        # Message metadata
        self.m_iMsgSize = 0
        self.m_iMsgYear = 0
        self.m_iMsgMonth = 0
        self.m_iMsgDay = 0
        self.m_iMsgErr = 0

        self.m_iBufSize = msg_size if msg_size > 0 else 8000

        self.m_iMsgCode = 0

        self.m_cpBuf = bytearray(msg_size)

        self.m_iSysNo = 0
        self.m_iCustSession = 0
        self.SellingDate = ""
        self.m_iMsgErrwu = 0
        self.m_iMsgTime = 0
        self.txnidd = 0
        self.m_iMsgSellTime = 0
        self.m_MsgBizDate = 0
        self.m_iSysName = ""

    def printMySelf(self):
        print(f"m_iMsgSize: {self.m_iMsgSize}")
        print(f"m_iMsgYear: {self.m_iMsgYear}")
        print(f"m_iMsgMonth: {self.m_iMsgMonth}")
        print(f"m_iMsgDay: {self.m_iMsgDay}")
        print(f"m_iMsgErr: {self.m_iMsgErr}")
        print(f"m_iBufSize: {self.m_iBufSize}")
        print(f"m_iMsgCode: {self.m_iMsgCode}")
        print(f"m_cpBuf: {self.m_cpBuf}")
        print(f"m_iSysNo: {self.m_iSysNo}")
        print(f"m_iCustSession: {self.m_iCustSession}")
        print(f"SellingDate: {self.SellingDate}")
        print(f"m_iMsgErrwu: {self.m_iMsgErrwu}")
        print(f"m_iMsgTime: {self.m_iMsgTime}")
        print(f"txnidd: {self.txnidd}")
        print(f"m_iMsgSellTime: {self.m_iMsgSellTime}")
        print(f"m_MsgBizDate: {self.m_MsgBizDate}")
        print(f"m_iSysName: {self.m_iSysName}")