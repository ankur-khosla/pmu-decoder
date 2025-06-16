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