"""
Data structures for parsing betting transaction logs.

This module contains ctypes structure definitions that map to the C/C++ data structures
used in the betting system's transaction logs. The structures follow the exact memory
layout and packing of the original C++ structures.

Key structures:
- PAYLOAD_HDR: Header containing metadata about the transaction payload
- LOGAB_HDR: Header containing transaction-specific metadata 
- LOGAB_DATA: Union containing the actual transaction data
- LOGAB: Top-level structure combining header and data

The structures use LittleEndianStructure/Union as the base classes to match the 
byte ordering of the source system.

Note: Many structure fields use custom bit fields and unions to exactly match the 
memory layout of the C++ structures. Field names are kept as close as possible to
the original C++ names for easier cross-referencing.
"""

from ctypes import (
    LittleEndianStructure, LittleEndianUnion, c_short, c_ushort, c_ubyte, c_uint, c_int32,
    c_longlong, c_ulonglong
)

# C Type Mappings:
# short                 -> c_short
# unsigned short        -> c_ushort
# unsigned char         -> c_ubyte
# unsigned int          -> c_uint
# __time32_t            -> c_int32
# LONGLONG              -> c_longlong

# 
# FOR Payload Header
#
PAYLOAD_HDR_SIZE = 35 #(Size of PAYLOAD_HDR in bytes in C++)
class PAYLOAD_HDR(LittleEndianStructure):
    """
    struct PAYLOAD_HDR
    {
        unsigned int system_id;
        unsigned int business_date;
        unsigned long long activity_id;
        unsigned long long cust_session_id; // customer session id. added in DEC2022 R1a for EDW
        unsigned int enquiry_status;
        unsigned char activity_nature;
        unsigned short sequence_num;
        unsigned short activity_total_num;
        unsigned short extra_data_len;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("system_id", c_uint),
        ("business_date", c_uint),
        ("activity_id", c_ulonglong),
        ("cust_session_id", c_ulonglong),
        ("enquiry_status", c_uint),
        ("activity_nature", c_ubyte),
        ("sequence_num", c_ushort),
        ("activity_total_num", c_ushort),
        ("extra_data_len", c_ushort),
    ]

# 
# FOR LOGAB_HDR
#

class LOGAB_SOURCE_VOICE(LittleEndianStructure):
    """
    struct LOGAB_SOURCE_VOICE
    {
      unsigned char   febu;
      unsigned short  termwu;
      unsigned int    locidlu;
      unsigned char train1 : 1;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("febu", c_ubyte),
        ("termwu", c_ushort),
        ("locidlu", c_uint),
        ("train1", c_ubyte, 1),
    ]


class LOGAB_SOURCE_DID(LittleEndianStructure):
    """
    struct LOGAB_SOURCE_DID
    {
     unsigned int    citlu;
      unsigned char   termbu;
      unsigned char   febu;
      unsigned char   citTypebu;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("citlu", c_uint),
        ("termbu", c_ubyte),
        ("febu", c_ubyte),
        ("citTypebu", c_ubyte),
    ]


class LOGAB_SOURCE_CBBT(LittleEndianStructure):
    """
    struct LOGAB_SOURCE_CBBT
    {
      unsigned int    centrelu:24;
      unsigned int    csctrn:1;
      unsigned int    ewallettrn : 1;
      unsigned int    unused:6;
      unsigned short  windowwu;
      unsigned short  ltnwu;
      unsigned char   cbbu;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("centrelu", c_uint, 24),
        ("csctrn", c_uint, 1),
        ("ewallettrn", c_uint, 1),
        ("unused", c_uint, 6),
        ("windowwu", c_ushort),
        ("ltnwu", c_ushort),
        ("cbbu", c_ubyte),
    ]


class LOGAB_SOURCE_OLD(LittleEndianStructure):
    """
    struct LOGAB_SOURCE_OLD
    {
      unsigned int    centrelu;
      unsigned short  windowwu;
      unsigned short  chanwu;
      unsigned char   cbbu;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("centrelu", c_uint),
        ("windowwu", c_ushort),
        ("chanwu", c_ushort),
        ("cbbu", c_ubyte),
    ]


class LOGAB_SOURCE_POL(LittleEndianStructure):
    """
    struct LOGAB_SOURCE_POL
    {
      unsigned char   filebu;
      unsigned int    offsetlu;
      unsigned int    skpAca1:1;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("filebu", c_ubyte),
        ("offsetlu", c_uint),
        ("skpAca1", c_uint, 1),
    ]


class LOGAB_SOURCE_DATA(LittleEndianUnion):
    """
    union LOGAB_SOURCE_DATA
    {
      struct LOGAB_SOURCE_VOICE  voice;
      struct LOGAB_SOURCE_DID    did;
      unsigned int               matlu;
      struct LOGAB_SOURCE_CBBT   cbBt;
      struct LOGAB_SOURCE_OLD    old;
      unsigned short             tbwu;
      struct LOGAB_SOURCE_POL    pol;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("voice", LOGAB_SOURCE_VOICE),
        ("did", LOGAB_SOURCE_DID),
        ("matlu", c_uint),
        ("cbBt", LOGAB_SOURCE_CBBT),
        ("old", LOGAB_SOURCE_OLD),
        ("tbwu", c_ushort),
        ("pol", LOGAB_SOURCE_POL),
    ]


class LOGAB_SOURCE(LittleEndianStructure):
    """
    struct LOGAB_SOURCE
    {
      unsigned char             srcTypebu;
      union LOGAB_SOURCE_DATA   data;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("srcTypebu", c_ubyte),
        ("data", LOGAB_SOURCE_DATA),
    ]


class LOGAB_HDR(LittleEndianStructure):
    """
    struct LOGAB_HDR
    {
      short                 sizew;
      unsigned short        codewu;
      unsigned short        errorwu;
      unsigned char         trapcodebu;
      unsigned int          stafflu;
      unsigned int          ltnlu;
      unsigned int          acclu;
      unsigned char         filebu;
      unsigned int          blocklu;
      unsigned int          overflowlu;
      unsigned short        offwu;
      unsigned short        tranwu;
      __time32_t            timelu;
      LONGLONG              lgslu;
      unsigned int          msnlu;
      struct LOGAB_SOURCE   source;
      unsigned char         extSysTypebu;
      unsigned short        catchup1:1;
      unsigned short        btexc1:1;
      unsigned short        othsys1:1;
      unsigned short        prelog1:1;
      unsigned short        timeout1:1;
      unsigned short        laterpy1:1;
      unsigned short        bcsmsg1:1;
      unsigned short        rcvmsg1:1;
      unsigned short        overflow1:1;
      unsigned short        escRel1:1;
      unsigned short        noFlush1:1;
      unsigned short        train1:1;
      unsigned short        sessionInfo1:1;
      unsigned short        uptacc1:1;
      unsigned short        anonymous1:1;
      unsigned short        :1;
      unsigned int 			bizdatelu;
      unsigned short 		ticketTypewu;
      LONGLONG				activityIdd;
      LONGLONG              termSessIdd;
      LONGLONG              custSessIdd;
      LONGLONG				txnidd;
      unsigned short  		txnCodewu;
      unsigned int          globalltnlu;
      LONGLONG              canceltxnidd;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("sizew", c_short),
        ("codewu", c_ushort),
        ("errorwu", c_ushort),
        ("trapcodebu", c_ubyte),
        ("stafflu", c_uint),
        ("ltnlu", c_uint),
        ("acclu", c_uint),
        ("filebu", c_ubyte),
        ("blocklu", c_uint),
        ("overflowlu", c_uint),
        ("offwu", c_ushort),
        ("tranwu", c_ushort),
        ("timelu", c_int32),
        ("lgslu", c_longlong),
        ("msnlu", c_uint),
        ("source", LOGAB_SOURCE),
        ("extSysTypebu", c_ubyte),
        ("catchup1", c_ushort, 1),
        ("btexc1", c_ushort, 1),
        ("othsys1", c_ushort, 1),
        ("prelog1", c_ushort, 1),
        ("timeout1", c_ushort, 1),
        ("laterpy1", c_ushort, 1),
        ("bcsmsg1", c_ushort, 1),
        ("rcvmsg1", c_ushort, 1),
        ("overflow1", c_ushort, 1),
        ("escRel1", c_ushort, 1),
        ("noFlush1", c_ushort, 1),
        ("train1", c_ushort, 1),
        ("sessionInfo1", c_ushort, 1),
        ("uptacc1", c_ushort, 1),
        ("anonymous1", c_ushort, 1),
        ("unused_bit", c_ushort, 1),
        ("bizdatelu", c_uint),
        ("ticketTypewu", c_ushort),
        ("activityIdd", c_longlong),
        ("termSessIdd", c_longlong),
        ("custSessIdd", c_longlong),
        ("txnidd", c_longlong),
        ("txnCodewu", c_ushort),
        ("globalltnlu", c_uint),
        ("canceltxnidd", c_longlong), 
    ] 





# 
# FOR LOGAB / LOGAB_DATA READING
#
# Since the relate structs and unions are too many in count,
# we will only define the ones that are relevant to APRace
# 
# APRace only access the followings:
# •	data.bt.rac.crossSellFl
# •	data.bt.rac.tran.bet.csctrn
# •	data.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.baseinv
# •	data.bt.rac.tran.bet.d.hdr.betinvcomb.flexi.flexibet
# •	data.bt.rac.tran.bet.d.hdr.bettypebu
# •	data.bt.rac.tran.bet.d.hdr.costlu
# •	data.bt.rac.tran.bet.d.hdr.sellTime
# •	data.bt.rac.tran.bet.d.hdr.totdu
# •	data.bt.rac.tran.bet.d.var.a.day
# •	data.bt.rac.tran.bet.d.var.a.evtbu
# •	data.bt.rac.tran.bet.d.var.a.fmlbu
# •	data.bt.rac.tran.bet.d.var.a.loc
# •	data.bt.rac.tran.bet.d.var.a.md
# •	data.bt.rac.tran.bet.d.var.a.sel.bettypebu
# •	data.bt.rac.tran.bet.d.var.a.sel.comwu
# •	data.bt.rac.tran.bet.d.var.a.sel.ind.bnk1
# •	data.bt.rac.tran.bet.d.var.a.sel.ind.fld1
# •	data.bt.rac.tran.bet.d.var.a.sel.ind.mbk1
# •	data.bt.rac.tran.bet.d.var.a.sel.ind.mul1
# •	data.bt.rac.tran.bet.d.var.a.sel.ind.rand1
# •	data.bt.rac.tran.bet.d.var.a.sel.pftrlu
# •	data.bt.rac.tran.bet.d.var.a.sel.racebu
# •	data.bt.rac.tran.bet.d.var.a.sel.sellu
# •	data.bt.rac.tran.bet.d.var.es.betexbnk.bnkbu
# •	data.bt.rac.tran.bet.d.var.es.day
# •	data.bt.rac.tran.bet.d.var.es.ind.bnk1
# •	data.bt.rac.tran.bet.d.var.es.ind.fld1
# •	data.bt.rac.tran.bet.d.var.es.ind.mbk1
# •	data.bt.rac.tran.bet.d.var.es.ind.mul1
# •	data.bt.rac.tran.bet.d.var.es.ind.rand1
# •	data.bt.rac.tran.bet.d.var.es.loc
# •	data.bt.rac.tran.bet.d.var.es.md
# •	data.bt.rac.tran.bet.d.var.es.racebu
# •	data.bt.rac.tran.bet.d.var.es.sellu
# 


class BETFLEXICOMBO(LittleEndianStructure):
    """
    struct BETFLEXICOMBO
    {
        unsigned int	baseinv:31;	// flexibet=0; BASE investment in dollar; flexibet = 1; noofcombination
        unsigned int	flexibet:1;	// flexi bet	
    };
    """
    _pack_ = 1
    _fields_ = [
        ("baseinv",  c_uint, 31),  # base investment in dollars (or number of combos when flexibet=1)
        ("flexibet", c_uint, 1),   # flexi‐bet flag
    ]

class BETINVESTCOMBO(LittleEndianUnion):
    """
    union BETINVESTCOMBO
    {
        //unsigned int	baseinv:31;	// flexibet=0; BASE investment in dollar; flexibet = 1; noofcombination
        //unsigned int	flexibet:1;	// flexi bet	
        struct BETFLEXICOMBO flexi;

        unsigned int    binvlu;         // base investment in dollar. added by in sp3. 2016.10.20
    };
    """
    _pack_ = 1
    _fields_ = [
        ("flexi",  BETFLEXICOMBO),  # flexi‐bet combination
        ("binvlu", c_uint),         # base investment in dollars
    ]

class BETIND(LittleEndianStructure):
    """
    struct  BETIND          // indicator
    {
        unsigned char  bnk1:1; // banker
        unsigned char  fld1:1; // field
        unsigned char  mul1:1; // multiple
        unsigned char  mbk1:1; // multiple banker
        unsigned char  rand1:1;// randomly generated
        unsigned char  :2;
        unsigned char  twoentry:1;// randomly generated
    
    };
    """
    _pack_ = 1
    _fields_ = [
        ("bnk1",     c_ubyte, 1),
        ("fld1",     c_ubyte, 1),
        ("mul1",     c_ubyte, 1),
        ("mbk1",     c_ubyte, 1),
        ("rand1",    c_ubyte, 1),
        ("_reserved",c_ubyte, 2),
        ("twoentry", c_ubyte, 1),
    ]    

BET_MLP_MAXLEG = 6
BET_BNKM_MAXLEG = 3   
BET_RAC_MAXSMAP = 2 
BET_AUP_MAXEVT = 6

class BETAUPSEL(LittleEndianStructure):
    """
    struct  BETAUPSEL       // extended allup info per event
    {
        unsigned char         racebu;         // race #
        unsigned char         bettypebu;      // non-allup bet type
        struct BETIND         ind;            // indicator
        unsigned long long		pid[BET_RAC_MAXSMAP];	// pool id
        unsigned char			fdsz;					// field size
        unsigned long long      sellu[BET_RAC_MAXSMAP]; // selection bitmap
        unsigned short        comwu;          // # of combinations
        unsigned int          pftrlu;         // pay factor
    };
    """
    _pack_ = 1
    _fields_ = [
        ("racebu",    c_ubyte),
        ("bettypebu", c_ubyte),
        ("ind",       BETIND),
        ("pid",       c_ulonglong * BET_RAC_MAXSMAP),
        ("fdsz",      c_ubyte),
        ("sellu",     c_ulonglong * BET_RAC_MAXSMAP),
        ("comwu",     c_ushort),
        ("pftrlu",    c_uint),
    ]

class BETAUP(LittleEndianStructure):
    """
    struct  BETAUP          // allup selections
    {
        unsigned char			loc;			// location
        unsigned char			day;			// Day
        int32_t			md;				// meeting day
        unsigned char         evtbu;          // # of events
        unsigned char         fmlbu;          // formula
        struct BETAUPSEL      sel[BET_AUP_MAXEVT];    // selections
    };
    """
    _pack_ = 1
    _fields_ = [
        ("loc",   c_ubyte),                             # location
        ("day",   c_ubyte),                             # day
        ("md",    c_int32),                             # meeting day
        ("evtbu", c_ubyte),                             # number of events
        ("fmlbu", c_ubyte),                             # formula
        ("sel",   BETAUPSEL * BET_AUP_MAXEVT),          # selections array
    ]



class BETEXBNK(LittleEndianUnion):
    """
    union BETEXBNK
    {
        unsigned long long      sellu[BET_MLP_MAXLEG];  // selection bitmap
        unsigned char         bnkbu[BET_BNKM_MAXLEG]; // # of bankers per leg [max. 3 legs]
    };
    """
    _pack_ = 1
    _fields_ = [
        ("sellu", c_ulonglong * BET_MLP_MAXLEG),
        ("bnkbu", c_ubyte     * BET_BNKM_MAXLEG),
    ]

class BETEXOSTD(LittleEndianStructure):
    """
    struct  BETEXOSTD       // exotic or standard info
    {
        unsigned char			loc;			// location
        unsigned char			day;			// day
        int32_t				md;			    // meeting date
        unsigned char			racebu;         // race #
        struct BETIND			ind;            // indicator
        unsigned long long		pid[BET_RAC_MAXSMAP];	// pool id
        unsigned char			fdsz[BET_MLP_MAXLEG];	// field size
        unsigned long long        sellu[BET_MLP_MAXLEG];  // selection bitmap
        union BETEXBNK			betexbnk;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("loc",     c_ubyte),
        ("day",     c_ubyte),
        ("md",      c_int32),
        ("racebu",  c_ubyte),
        ("ind",     BETIND),
        ("pid",     c_ulonglong * BET_RAC_MAXSMAP),
        ("fdsz",    c_ubyte * BET_MLP_MAXLEG),
        ("sellu",   c_ulonglong * BET_MLP_MAXLEG),
        ("betexbnk", BETEXBNK),
    ]

class BETVAR(LittleEndianUnion):
    """
    union   BETVAR                          // variable part
    {
        struct BETAUP         a;      // allup
        struct BETEXOSTD      es;     // exotic/standard
        struct BETLOT         lot;    // lottery  // ** NOT RELEVANT TO APRace **
        struct BETDEP         cv;     // cash voucher ** NOT RELEVANT TO APRace **
        struct BETSB_DET      sb;     // soccer betting ** NOT RELEVANT TO APRace **
    };
    """
    _pack_ = 1
    _fields_ = [
        ("a",   BETAUP),      
        ("es",  BETEXOSTD)
    ]

class BETHDR(LittleEndianStructure):
    """
    struct  BETHDR                          // common header
    {
        unsigned LONGLONG     totdu;          // total payout in cents
        union BETINVESTCOMBO	betinvcomb;		// Q308 changes
        unsigned int     costlu;         // total cost in cents
        int32_t                sellTime;       // sell time
        unsigned int			businessDate;		// business date
        unsigned char         bettypebu;      // bet type
        struct BETSTS         sts;            // ** NOT RELEVANT TO APRace **
    };
    """
    _pack_ = 1
    _fields_ = [
        ("totdu",        c_ulonglong),
        ("betinvcomb",   BETINVESTCOMBO),
        ("costlu",       c_uint),
        ("sellTime",     c_int32),
        ("businessDate", c_uint),
        ("bettypebu",    c_ubyte),
        ("_padding_BETSTS", c_ubyte * 2)
    ]


class BETDATA(LittleEndianStructure):
    """
    struct BETDATA
    {
        struct BETHDR         hdr;    // common header
        union BETVAR          var;    // variable part
    };
    """
    _pack_ = 1
    _fields_ = [
        ("hdr", BETHDR),
        ("var", BETVAR),
    ]


class BETABRAC(LittleEndianStructure):
    """
    struct BETABRAC
    {
        unsigned char   srcbu:6;    // source of sell (Changed 201108PSR)
        unsigned char   blc1:1;  // Transaction with CSC Card (Added 201108PSR); triggers control
        unsigned char   csctrn : 1;  // Transaction with CSC Card (Added 201108PSR)
        //int32_t          dat;      // meeting date
        //unsigned char   locbu;    // location
        //unsigned char   daybu;    // day
        struct BETDATA  d;        // data
    };
    """
    _pack_ = 1
    _fields_ = [
        ("srcbu",   c_ubyte, 6),  # source of sell
        ("blc1",    c_ubyte, 1),  # CSC card transaction flag
        ("csctrn",  c_ubyte, 1),  # CSC card control flag
        ("d",       BETDATA),     # data payload
    ]


class ACU_TRAN_RAC2(LittleEndianStructure):
    """
    struct ACU_TRAN_RAC2
    {
        unsigned int     content;
        struct BETABRAC  bet;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("content", c_uint),
        ("bet",    BETABRAC),
    ]

class LOGABRAC_BET_ERR(LittleEndianStructure):
    """
    //Q308 changes.
    //2011IBT change the name (LOGAB_ERROR_INFO --> LOGABRAC_BET_ERR)
    struct LOGABRAC_BET_ERR
    {
        unsigned int	   minbettot;      // Minimum bet total in cents on error "total min. investment not met"    
        unsigned char      racebu;     // error race number
        unsigned char      selbu;      // error selection
    };
    """
    _pack_ = 1
    _fields_ = [
        ("minbettot", c_uint),  # minimum bet total in cents on error
        ("racebu",    c_ubyte), # error race number
        ("selbu",     c_ubyte), # error selection
    ]


class LOGABRAC_BET_UPD(LittleEndianStructure):
    """
    struct LOGABRAC_BET_UPD
    {
        unsigned int				offsetlu;   //offset of bet in file		
        unsigned int				tranamt;    //Transferred amount (In cents) (201108PSR - changed from short to int)
    };
    """
    _pack_ = 1
    _fields_ = [
        ("offsetlu", c_uint),
        ("tranamt",  c_uint),
    ]    

class LOGABRAC_BET_INFO(LittleEndianUnion):
    """
    union LOGABRAC_BET_INFO
    {
        struct LOGABRAC_BET_UPD		raceinfo;   // Race Sell Bet info (2011IBT Changes)
        struct LOGABRAC_BET_ERR		errorinfo;	// error info  
    };
    """
    _pack_ = 1
    _fields_ = [
        ("raceinfo", LOGABRAC_BET_UPD),
        ("errorinfo", LOGABRAC_BET_ERR),
    ]

class LOGAB_RAC(LittleEndianStructure):
    """
    struct LOGAB_RAC
    {
        union LOGABRAC_BET_INFO betinfo;
        unsigned short        indexwu;    // meeting index
        unsigned char			crossSellFl:1; // cross sell indicator
        unsigned char			:7;
        struct ACU_TRAN_RAC2   tran;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("betinfo",     LOGABRAC_BET_INFO),
        ("indexwu",     c_ushort), 
        ("crossSellFl", c_ubyte, 1),  
        ("_reserved", c_ubyte, 7),     # keep the padding
        ("tran", ACU_TRAN_RAC2),
    ]

class ACU_TRAN_DEP(LittleEndianStructure):
    """
    struct ACU_TRAN_DEP
    {
    int32_t             holdtime;      // release time for withdrawal
    unsigned LONGLONG  amountdu;      // amount
    unsigned LONGLONG  chargedu;      // service charge
    unsigned char      typebu;        // deposit type
        #define ACU_DEP_CASH  1
        #define ACU_DEP_CIT   2
        #define ACU_DEP_MPT   3
        #define ACU_DEP_ATM   4
        #define ACU_DEP_PAY   5         // payout deposit
        #define ACU_DEP_CHQ   6         // cheque
        #define ACU_DEP_ITN   7         // internet
        #define ACU_DEP_FPS   22         // FPS
    unsigned char       hold1:1;       // withholdable
    unsigned char       cancel1:1;     // cancelled
    unsigned char       reversed1:1;   // reversed
    unsigned char       released1:1;   // released (ignore hold time)
    //unsigned char       secondnba1:1;   // Transaction on secondary NBA
    //unsigned char       ertregno1:1;   // ERT registration number captured
    unsigned char       csctrn:1;   // Transaction by CSC (Added 201108PSR)
    unsigned char      srcbu;         // source of deposit; defined in LOGDEF_AB.H
    };
    """
    _pack_ = 1
    _fields_ = [
        ("holdtime",   c_int32),       # release time for withdrawal
        ("amountdu",   c_ulonglong),   # amount
        ("chargedu",   c_ulonglong),   # service charge
        ("typebu",     c_ubyte),       # deposit type (ACU_DEP_…)
        # bit‐fields share one byte:
        ("hold1",      c_ubyte, 1),    # withholdable
        ("cancel1",    c_ubyte, 1),    # cancelled
        ("reversed1",  c_ubyte, 1),    # reversed
        ("released1",  c_ubyte, 1),    # released (ignore hold time)
        ("csctrn",     c_ubyte, 1),    # transaction by CSC
        ("_reserved",  c_ubyte, 3),    # padding
        ("srcbu",      c_ubyte),       # source of deposit
    ]

class BETABLOT(LittleEndianStructure):
    """
    struct BETABLOT
    {
        unsigned char   srcbu:7;    // source of sell (Changed 201108PSR)
        unsigned char   csctrn:1;  // Transaction with CSC Card (Added 201108PSR)
        //unsigned short  yearwu;   // year
        //unsigned short  drawwu;   // draw #
        //unsigned short  typewu;   // type of lottery
        struct BETDATA  d;        // data
    };    
    """
    _pack_ = 1
    _fields_ = [
        ("srcbu",  c_ubyte, 7),  # source of sell (7 bits)
        ("csctrn", c_ubyte, 1),  # CSC card transaction (1 bit)
        ("d",      BETDATA),     # bet data
    ]

class ACU_TRAN_LOT2(LittleEndianStructure):
    """
    struct ACU_TRAN_LOT2
    {
    unsigned int     content;
    struct BETABLOT  bet;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("content", c_uint),   # content field
        ("bet",     BETABLOT), # bet details
    ]

class LOGAB_LOT(LittleEndianStructure):
    """
    struct LOGAB_LOT
    {
    unsigned short        indexwu;    // lottery index
    unsigned char			ndrawbu;		// number of draw
    unsigned short        selwu;      // error selection
    unsigned char			versionbu;	// version number
    unsigned int          offsetlu;   // offset of bet in file
    unsigned char			multidraw:1;  // multi-draw flag q207
    unsigned char			crossSellFl:1;  // cross sell indicator 
    unsigned char			test:6;
    unsigned int          mintktcost;   // (201108PSR, Reject=min total ticket;Success=Transfer Amt;Other Situation=0)
    struct ACU_TRAN_LOT2   tran;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("indexwu",    c_ushort),    # lottery index
        ("ndrawbu",    c_ubyte),     # number of draw
        ("selwu",      c_ushort),    # error selection
        ("versionbu",  c_ubyte),     # version number
        ("offsetlu",   c_uint),      # offset of bet in file
        ("multidraw",  c_ubyte, 1),  # multi-draw flag q207
        ("crossSellFl",c_ubyte, 1),  # cross sell indicator
        ("test",       c_ubyte, 6),  # reserved
        ("mintktcost", c_uint),      # min total ticket / transfer amt
        ("tran",       ACU_TRAN_LOT2),
    ]

class ACU_TRAN_WTW(LittleEndianStructure):
    """
    struct ACU_TRAN_WTW
    {
    LONGLONG           amountd;   // amount
    unsigned LONGLONG  chargedu;  // service charge
    unsigned char      typebu;    // withdrawal type  
        #define ACU_WTW_AUTOPAY  1
        #define ACU_WTW_CHEQUE   2
        #define ACU_WTW_BANK     3  // online 
        #define ACU_WTW_CASH     4
        #define ACU_WTW_FPS		 6	//FPS
    unsigned char      actBybu;   // activated by
        #define ACU_WTW_TBTR     1
        #define ACU_WTW_MAT      2
        #define ACU_WTW_SI       3
        #define ACU_WTW_AUTO     4
        #define ACU_WTW_MPT      5
        #define ACU_WTW_CIT      6
        #define ACU_WTW_CB       7
        #define ACU_WTW_ITN      8  // internet
    unsigned char      srcbu;     // source of withdrawal; defined in LOGDEF_AB.H
    unsigned char       cancel1:1; // cancelled
    // unsigned char       ertcaptured1:1; // ERT registration number captured
    unsigned char       csctrn:1;  // Transaction with CSC Card (Added 201108PSR)
    unsigned char       undo :1; //undo added for sp21a
    unsigned char       :5;        // Unused (Changed 201108PSR)
    };
    """
    _pack_ = 1
    _fields_ = [
        ("amountd",   c_longlong),    # amount
        ("chargedu",  c_ulonglong),   # service charge
        ("typebu",    c_ubyte),       # withdrawal type (ACU_WTW_…)
        ("actBybu",   c_ubyte),       # activated by (ACU_WTW_…)
        ("srcbu",     c_ubyte),       # source of withdrawal
        # bit‐fields share one byte:
        ("cancel1",   c_ubyte, 1),    # cancelled
        ("csctrn",    c_ubyte, 1),    # CSC card transaction
        ("undo",      c_ubyte, 1),    # undo (SP21a)
        ("_reserved", c_ubyte, 5),    # unused
    ]

class LOGAB_WTW_UNION(LittleEndianUnion):
    """
    See LOGAB_WTW below for the union definition
    """
    _pack_ = 1
    _fields_ = [
        ("__padding_LOGAB_EPS_TB", c_ubyte * 1912),
        ("__padding_LOGAB_FPS", c_ubyte * 792),
        ("divprocddtlu", c_uint),    # Amount in dollar deducted from dividend pocket
    ]

class LOGAB_WTW(LittleEndianStructure):
    """
    struct LOGAB_WTW
    {   
        struct ACU_TRAN_WTW   tran;       // withdrawal transaction in account file
        union {
            struct LOGAB_EPS_TB   eps;      // eps information                 // EH07
            struct LOGAB_FPS		fps;		// FPS
            unsigned int			divprocddtlu;  // Amount in dollar deducted from dividend pocket;0=normal a/c> 0 for IBT anonymous a / c only
        };
    };
    """
    _pack_ = 1
    _fields_ = [
        ("tran", ACU_TRAN_WTW),      # withdrawal transaction in account file
        ("_union", LOGAB_WTW_UNION),  # nested union of eps/fps/divprocddtlu
    ]

class LOGAB_SBMSG(LittleEndianStructure):
    """
    struct LOGAB_SBMSG
    {
        unsigned int		minTktTot;                   // Q310 Minimun Ticket Total 
        unsigned short        lenwu;                      // terminal data length
        unsigned char         trmDatabu[450];  // terminal data [variable]
    };
    """
    _pack_ = 1
    _fields_ = [
        ("minTktTot", c_uint),
        ("lenwu",     c_ushort),
        ("trmDatabu", c_ubyte * 450),
    ]

class ACU_TRAN_SB2(LittleEndianStructure):
    """
    struct ACU_TRAN_SB2
    {
    union  TSN      tsn;
    unsigned char   srcbu:7;    // source of sell (Changed 201108PSR)
    unsigned char   csctrn:1;  // Transaction with CSC Card (Added 201108PSR)
    struct BETDATA  bet;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("_padding_TSN", c_ubyte * 10),         # transaction sequence number union
        ("srcbu",  c_ubyte, 7),    # source of sell (7 bits)
        ("csctrn", c_ubyte, 1),    # transaction with CSC card (1 bit)
        ("bet",    BETDATA),       # bet details
    ]

class LOGAB_SBBET(LittleEndianStructure):
    """
    struct LOGAB_SBBET
    {
    unsigned short          oddOut1:1;      // odds outdated
    unsigned short          woodds1:1;      // selling without odds
    unsigned short          bonus1:1;       // bonus flag
    unsigned short          rconfirm1:1;    // require confirm by customer
    unsigned short          chgodds1:1;     // odds changed
    unsigned short          chgubet1:1;     // unit bet changed
    unsigned short          intercept1:1;   // bet intercept at rm
    unsigned short          settle1:1;      // bet settled with SB
    unsigned short          abort1:1;       // user abort request recieved
    unsigned short          confirm1:1;     // user confirmed request
    unsigned short		  crossSellFl:1; // cross sell indicator
    unsigned short          :5;
    struct SBLOG_BET_ERR  err;            // sb account type for some error (Reviewed 201108PSR)
    unsigned char         sbtypbu;        // sb account type
    unsigned char			sbmsgver;		// sb message version no.	Q405
    unsigned short        lenwu;          // sb bet size
    struct ACU_TRAN_SB2    tran;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("oddOut1",     c_ushort, 1),
        ("woodds1",     c_ushort, 1),
        ("bonus1",      c_ushort, 1),
        ("rconfirm1",   c_ushort, 1),
        ("chgodds1",    c_ushort, 1),
        ("chgubet1",    c_ushort, 1),
        ("intercept1",  c_ushort, 1),
        ("settle1",     c_ushort, 1),
        ("abort1",      c_ushort, 1),
        ("confirm1",    c_ushort, 1),
        ("crossSellFl", c_ushort, 1),
        ("_reserved",   c_ushort, 5),
        ("_padding_SBLOG_BET_ERR", c_ubyte * 12),  # sb account error info
        ("sbtypbu",     c_ubyte),
        ("sbmsgver",    c_ubyte),
        ("lenwu",       c_ushort),
        ("tran",        ACU_TRAN_SB2),
    ]

class LOGAB_SB(LittleEndianUnion):
    """
    union LOGAB_SB
    {
        struct LOGAB_SBMSG   msg;         // terminal message
        struct LOGAB_SBBET   bet;         // reply
    };
    """
    _pack_ = 1
    _fields_ = [
        ("msg", LOGAB_SBMSG),   # terminal message
        ("bet", LOGAB_SBBET),   # reply
    ]

class LOGAB_DEP(LittleEndianStructure):
    """
    struct LOGAB_DEP
    {
    struct ACU_TRAN_DEP   tran;       // transaction in account file
    union LOGAB_DEP_DATA  data;       // deposit detail
    };
    """
    _pack_ = 1
    _fields_ = [
        ("tran", ACU_TRAN_DEP),
        ("_padding_LOGAB_DEP_DATA", c_ubyte * 1912)
    ]

class LOGAB_CAN_DATA(LittleEndianUnion):
    """
    union LOGAB_CAN_DATA
    {
    struct LOGAB_LOT    lot;
    struct LOGAB_RAC    rac;
    struct LOGAB_WTW    wtw;
    union  LOGAB_SB     sb;
    struct LOGAB_DEP    dep;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("lot", LOGAB_LOT),
        ("rac", LOGAB_RAC),
        ("wtw", LOGAB_WTW),
        ("sb",  LOGAB_SB),
        ("dep", LOGAB_DEP),
    ]

class LOGAB_CAN(LittleEndianStructure):
    """
    struct LOGAB_CAN
    {
    unsigned short        tranwu;         // cancelled transaction number
    unsigned short        codewu;         // cancelled transaction code ACU_CODE_...
    unsigned char         filebu;         // file # of account file [0=overflow]
    unsigned int          blocklu;        // block # of account file
    unsigned short        offwu;          // offset to account unit
    LONGLONG				rcltokend;		// token obtain from recall for cancel

    //unsigned int			token;			// q207
    int32_t				businessDate;	// q207

    unsigned char         otherUnit1:1;   // cancel on other unit
    unsigned char         canprv1:1;      // cancel earlier call
    unsigned char         byTsn1:1;       // cancel by TSN (ESC mode only)
    unsigned char			canPrevDay:1;	// cancel previous day q207
    LONGLONG				txnidd;			// SP3:cancelled transaction id
    unsigned int			verifierlu;		// SP3: segregate from block / offset

    union LOGAB_CAN_DATA  data;
    };
    """
    _pack_ = 1
    _fields_ = [
        ("tranwu",      c_ushort),    # cancelled transaction number
        ("codewu",      c_ushort),    # cancelled transaction code ACU_CODE_...
        ("filebu",      c_ubyte),     # file # of account file [0=overflow]
        ("blocklu",     c_uint),      # block # of account file
        ("offwu",       c_ushort),    # offset to account unit
        ("rcltokend",   c_longlong),  # token obtain from recall for cancel
        ("businessDate",c_int32),     # q207
        # bit‐fields packed into one byte:
        ("otherUnit1",  c_ubyte, 1),  # cancel on other unit
        ("canprv1",     c_ubyte, 1),  # cancel earlier call
        ("byTsn1",      c_ubyte, 1),  # cancel by TSN (ESC mode only)
        ("canPrevDay",  c_ubyte, 1),  # cancel previous day q207
        ("_reserved",   c_ubyte, 4),  # unused bits
        ("txnidd",      c_longlong),  # SP3: cancelled transaction id
        ("verifierlu",  c_uint),      # SP3: segregate from block / offset
        ("data",        LOGAB_CAN_DATA),
    ]


class LOGBT_AB(LittleEndianUnion):
    """
    // BT transactions
    union LOGBT_AB
    {
        struct LOGAB_SGN          sgn;        // signon
        struct LOGAB_SGF          sgf;        // signoff
        struct LOGAB_ACA          aca;        // account access
        struct LOGAB_ACR          acr;        // account release
        struct LOGAB_RAC          rac;        // race bet/enquiry
        struct LOGAB_LOT          lot;        // lottery bet/enquiry
        struct LOGAB_WTW          wtw;        // withdrawal
        struct LOGAB_DEP          dep;        // deposit
        struct LOGAB_CAN          can;        // cancel
        struct LOGAB_RCL          rcl;        // recall
        union  LOGAB_SB           sb;         // football bet/enquiry
        struct LOGAB_ADTLENQ      adtlenq;    // account detail enquiry
        struct LOGAB_CARDISS      esciss;     // issue esc card
        struct LOGAB_CARDREPL     escrep;     // replace esc card
        struct LOGAB_CARDRET      escret;     // return esc card
        struct LOGAB_CHGSCD       chgscd;     // bt charge security code
        struct LOGAB_AUTHVER      authver;    // authority verification 
        struct LOGAB_DEVISS       deviss;     // device issue
        struct LOGAB_DEVREPL      devrepl;    // device replace
        struct LOGAB_DEVCAN       devcan;     // device cancel
        struct LOGAB_ECVISS       ecviss;     // ECV issue
        struct LOGAB_ECVRET       ecvret;     // ECV return
        struct LOGAB_ECVCLSENQ    ecvclsenq;  // ECV close enquiry
        struct LOGAB_EFT_MISC     eftmisc;    // initialize EFT terminal
        struct LOGAB_EFT_LTEST    ltest;      // EFT link test
        struct LOGAB_CVI          cvi;        // CV issue via EFT
        struct LOGAB_ACCBAL       accbal;     // account balance via EFT, PAN capture
        struct LOGAB_RELTRM       reltrm;     // Release Terminal
        struct LOGAB_TXNENQ       txnenq;     // ticket enquiry
        struct LOGAB_ILL          ill;        // illegal message
        struct LOGAB_TERMBET		termb;		// terminate bet
        struct LOGAB_SMSCHG		smscharge;	// sms charge
        struct LOGAB_EFT_ACC_ACT	eftAccAct;	// sms charge
        struct LOGAB_EFT_ERT		eftert;		// EFT Ert
        struct LOGAB_CSCBAL		cscbal;		// CSC card balance (201108PSR)
        struct LOGAB_CSCRPL		cscrpl;		// CSC card replace (2011IBT)
        struct LOGAB_CSCRET		cscret;		// CSC card return (2011IBT)
    };
    # Only rac is relevant to APRace
    """
    _pack_ = 1
    _fields_ = [
        # Omitting the "at" onwards as it is not relevant to APRace
        ("rac", LOGAB_RAC),
        ("can", LOGAB_CAN)
    ]

class LOGAB_DATA(LittleEndianUnion):
    """
    union LOGAB_DATA
    {
    union  LOGBT_AB       bt;     // BT Txn
    union  LOGAT_AB       at;     // AT Txn
    union  LOGAB_POL      pol;    // pre-online
    union  LOGOTH         oth;    // others
    union  EODTRN_LOG     eod;    // eod tran   ! FT01
    struct LOGAB_DEPATM   deph;   // DEPHNDR log requests ! VC02
    struct LOGRDC         rdc;    // RDC message
    struct LOGSBC         sbc;    // SBC message
    };

    Omitting the "at" onwards
    """
    _pack_ = 1
    _fields_ = [
        ("bt", LOGBT_AB),
        ("_padding_LOGAT_AB", c_ubyte * 1006),
        ("_padding_LOGAT_POL", c_ubyte * 580),
        ("_padding_LOGOTH", c_ubyte * 84),
        ("_padding_EODTRN_LOG", c_ubyte * 593),
        ("_padding_LOGAB_DEPATM", c_ubyte * 117),
        ("_padding_LOGRDC", c_ubyte * 3843),
        ("_padding_LOGSBC", c_ubyte * 76),
    ]

class LOGAB(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("hdr", LOGAB_HDR),
        ("data", LOGAB_DATA),
    ]



### Some Additional Structures for Extra Data in Payload header
class EXTDTCOMMAB(LittleEndianStructure):
    """
    // Genaral Extra Data.
    // Sign-On/Sign-Off; Account Detail Enquiry; BT Change Security Code; Authority Verification; 
    // initialise EFT Terminal/Bank Balance; EFT link Test; CV Issue via EFT; Account Balance via EFT/PAN Capture;
    // Ticket Enquiry; Terminal Bet; Illegal Message; EFT Activation from TBAS; EFT ERT; Bank Account Number;
    // NBA Information; AT Transaction; Log others
    struct EXTDTCOMMAB
    {
        unsigned short		acterrwu;	// Activity error code; LOG.LOGHDR.errwu
        LONGLONG				actts;		// Activity timesstamp;  LOG.LOGHDR.timelu
    };
    """
    _pack_ = 1
    _fields_ = [
        ("acterrwu", c_ushort),
        ("actts",    c_longlong),
    ]

class EXTDTAB(LittleEndianStructure):
    """
    // Extra data.
    // Account Access; Account Release;  Withdrawal; Deposit; Cancel; Recall;
    // SB; Issue ESC Card; replace ESC Card; Return ESC Card;Device Issue; Device Replace; Device Cancel;
    // Release Terminal; SMS Charge;
    struct EXTDTAB
    {
        EXTDTCOMMAB extdtcomm;
        unsigned LONGLONG txnidd;	// transaction id. LOG.LOGHDR.txnidd;
    };    
    """
    _pack_ = 1
    _fields_ = [
        ("extdtcomm", EXTDTCOMMAB),
        ("txnidd",    c_longlong),
    ]

class EXTDTRLS(LittleEndianStructure):
    """
    // Race Bet; Lottery Bet; SB;
    struct EXTDTRLS
    {
        EXTDTAB extDTAB;
        LONGLONG	  sellTime; // selling time
        unsigned int bizdatelu; // business date

    };
    """
    _pack_ = 1
    _fields_ = [
        ("extDTAB",   EXTDTAB),
        ("sellTime",  c_longlong),
        ("bizdatelu", c_uint),
    ]