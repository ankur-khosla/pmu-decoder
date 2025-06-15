// Log record structure
#define LONGLONG long long

struct LOGAB
{
  struct LOGAB_HDR   hdr;   // header
  union LOGAB_DATA   data;  // data
};

// Log data structure
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

struct LOGAB_CSCRET     
{
  struct ACU_TRAN_ACA   tran;   //Account Access details
  unsigned char			wdtype;   // Withdrawal type
  struct AA_OLTP_CSCRETREQ   req;  //CSC Card Return Request
  struct LOGBCSAA           bcs;  // bcs info
  struct AA_OLTP_CSCRETRPY rpy;  //CSC Card Return Reply
};

struct AA_OLTP_CSCRETRPY
{
    unsigned LONGLONG   refamt;   // Refund amount for CSC card (in cents)
};

struct AA_OLTP_CSCRETREQ
{
    unsigned int        accno;  //Account number
    unsigned LONGLONG   cscid;  //CSC card ID
    unsigned char   fordep;  //Forfeit deposit (0=FALSE,1=TRUE)
    LONGLONG   accbal;  //Account Balance (in cents)
};


struct ACU_TRAN_ACA
{
  LONGLONG      fundd;    // funds available
  //LONGLONG      bankgd;   // bank guarentee
  LONGLONG		dpflag1 : 1;// bankgd stores dividend pocket (DP) instead of BG   // JC50
  LONGLONG		cscflag1 : 1;// CSC account access                                // CS52
  LONGLONG		ewalletflag1 : 1;// eWallet account access						  //SP21a
  LONGLONG		reserved : 13;                                                    // JC50
  LONGLONG      bankgd : 48;// bank guarentee (BG) or settled divdend pocket (DP) // JC50
  LONGLONG      curDivd;  // unsettled dividend
  LONGLONG      prvDivd;  // previous dividend
  LONGLONG      sbPFtd;   // soccer fo payout forfeited
};

struct LOGAB_CSCRPL
{
  struct ACU_TRAN_ACA   tran;   //Account Access details
  //struct LOGAB_SOURCE   source;  //This is for error only; no need to deocde for 2011IBT
  struct AA_OLTP_CSCRPLREQ   req;  //CSC Card Replace Request
  struct LOGBCSAA           bcs;  // bcs info
  struct AA_OLTP_CSCRPLRPY rpy;  //CSC Card Replace Reply
};

struct AA_OLTP_CSCRPLREQ
{
    unsigned int        accno;   // Account number
    unsigned LONGLONG   oldcscid;   // Old CSC card ID
    unsigned LONGLONG   newcscid;   // New CSC card ID
    unsigned char   fdepfee;   // Forfeit old card deposit fee (0=FALSE,1=TRUE)
    unsigned char   wdepfee;   // Waive new card deposit fee (0=FALSE,1=TRUE)
};

struct LOGAB_CSCBAL
{
  struct ACU_TRAN_ACA   tran;   //Account Access details
  unsigned char			lang;   //Language
  unsigned char			calltran;   //Call transfer (0=FALSE 1=TRUE)
  unsigned char			acctype;   //FB account type
  LONGLONG				amt;    //Current day expenditure amount (In cents)
  LONGLONG				div;    //Total dividend (In cents)
  unsigned char         staffbet:1;    // staff betting a/c
  unsigned char         :7;    // not used
  //struct LOGAB_SOURCE   source;  //This is for error only; no need to deocde for 201108PSR
};

struct LOGAB_EFT_ERT      
{
  struct LOGAB_NBA_INFO	nbainfo1;	//nba bank info 1
  struct LOGAB_NBA_INFO	nbainfo2;	//nba bank info 2	
  unsigned char			clearreg:1;   // registration nuber in databse to be cleared
  unsigned char			nba1status;   // primary nba status
  unsigned char			nba2status;   // secondary nba status
  struct LOGAB_EPS_TB	epstb;	//EPS information	
};

struct LOGAB_EPS_TB             // epsco info involving account/CIT
{
  union LOGAB_EPS_ACC   acc;        // account related info
  struct LOGAB_EPS_EGW  egw;        // eft gateway info [omitted if no
};     

union LOGAB_EPS_ACC                 // account/CIT related info
{
    struct LOGAB_EPS_CIT    cit;    // cit transaction
    struct LOGAB_EPS_EFT    eft;    // eft transaction from cb
};

struct LOGAB_EPS_CIT            // account related info in cit tran
{
  unsigned char         epinbu[8];  // epin
  unsigned char         ektbu[27];   // ekt
  unsigned char         msnbu;      // cit msn
  unsigned int          citlu;      // cit #
};

struct LOGAB_EPS_EFT            // account related info in eft tran
{
  unsigned int          seculu;     // security code
  unsigned char         esc1:1;     // ESC EFT transaction
  struct ACU_TRAN_ACA   aca;        // account access information
};

struct LOGAB_NBA_INFO
{
  unsigned char				nbatype;		// NBA type1=pri,2=sec
  struct ACU_BANKACCNUM		nbaacct;		// nba bank account number	
  unsigned char				channeltype;	// channel type (pin type) 0=no channel,1=IS,2=TB,3=BOTH
  char						RegNo[13];		// registration no. 

};

#define ACU_PAN_SIZE       19
#define ACU_BANK_ACN_SIZE  26
#define ACU_BANK_SIZE      3
#define ACU_BRANCH_SIZE    3
#define ACU_BNKACCNUM_SIZE 12
struct ACU_BANKACCNUM
{
  // char           bankAcns[ACU_BANK_ACN_SIZE+1];  // bank account #
  char           banks[ACU_BANK_SIZE+1];            // bank code
  char           branchs[ACU_BRANCH_SIZE+1];        // branch code
  char           bankAccNums[ACU_BNKACCNUM_SIZE+1]; // bank account #
};


struct LOGAB_EFT_ACC_ACT            // eft activation q108
{
  unsigned int				acctNo;		// account number 
  struct BCS_DATE			activateDate;	// activation date
  struct ACU_BANKACCNUM		nbaacct;	//primary nba bank account number	
  unsigned char				request:1;			// Q210 request from channel
  unsigned char				regno:1;			// registration number
  char						eftRegNo[13];		// eft registration no. 
};

struct BCS_DATE
{
    char    day;
    char    month;
    short   year;
};

struct LOGAB_SMSCHG             // account balance via EFT, PAN capture
{
  //unsigned int				amount;		// Amount  (Changed at 2011IBT)
  //unsigned int				nouse;		//  MAR2011 skipped  (Changed at 2011IBT)
  unsigned int				amount;		// Amount(In cents) (Changed at 2011IBT)
  BOOL						version;    // New version	0 = FALSE 1 = TRUE (Changed at 2011IBT)
  char						nouse[3];	// unused (Changed at 2011IBT)
  unsigned short			reasonCode;	// Reason of charge
  LONGLONG				    amt;  //Amount in cents. Anonymous acc only (201108PSR)
};


struct LOGAB_TERMBET             // account balance via EFT, PAN capture
{
  unsigned short			termTranNo;		// terminated transaction no
  unsigned short			termTranCode;	// terminated transaction no
  unsigned char				acctFileNo;		// 
  unsigned int				acctBlkNo;		// 
  unsigned short			offset;			// 
  LONGLONG				token;			// token
  unsigned long long			dividend;		// dividend paid at termination
  unsigned long long			refund;			// refund paid at termination
  unsigned long long			forfSbDiv;		// forfeited sb dividend
  int32_t					businessDate;	// 
  unsigned char             termOtherUnit:1; // 1 - terminate previous date
  unsigned char             termPrevDate:1;  // 1 - terminate previous date
  unsigned char				:7;				 // unused
  struct LOGAB_SBBET		sbbet;
};

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

struct ACU_TRAN_SB2
{
  union  TSN      tsn;
  unsigned char   srcbu:7;    // source of sell (Changed 201108PSR)
  unsigned char   csctrn:1;  // Transaction with CSC Card (Added 201108PSR)
  struct BETDATA  bet;
};

union   TSN
{
  struct TSN_A          s;      // structured
  unsigned short        w[5];
  struct TSN_SB         sb;     // soccer betting tsn
  struct TSN19T         s19t;
  struct TSN19A         s19a;
};

struct TSN19A
{
    struct TSN19A_1     w1;
    struct TSN19A_2     w2;
    unsigned short      acclwu;         // account number (lo bits)
    struct TSN19A_4     w4;
    struct TSN19_5      w5;
};

struct TSN19_5
{
    unsigned short        unused4:4;
    unsigned short        verifierl12:12; // content verifier (lo bits)
};


struct TSN19A_4
{
    unsigned short        tranl6:6;       // transaction number (lo bits)
    unsigned short        tsn16:1;        // TSN is 16 digits long (= 0 for TSN19)
    unsigned short        day9:9;         // meeting day/transaction day/draw number
};


struct TSN19A_1
{
    unsigned short        tranh6:6;       // transaction number (hi bits)
    unsigned short        type5:5;        // ticket type
    unsigned short        secu5:5;        // security code
};

struct TSN19A_2
{
    unsigned short        acclh14:14;     // account number (hi bits)
    unsigned short        tranm2:2;       // transaction number (mid bits)
};


struct TSN19T
{
    struct TSN19T_1     w1;
    struct TSN19T_2     w2;
    unsigned short      reclwu;         // record offset (lo bits)
    struct TSN19T_4     w4;
    struct TSN19_5      w5;
};

struct TSN19T_1
{
    unsigned short        loc3:3;         // meeting location/sales year
    unsigned short        sys3:3;         // sale system #
    unsigned short        type5:5;        // ticket type
    unsigned short        secu5:5;        // security code
};

struct TSN19T_2
{
    unsigned short        rech12:12;      // record offset (hi bits)
    unsigned short        reserved2:2;
    unsigned short        offUnit2:2;     // offset unit
                                        // 0 = word unit, 1 = 2-word unit,
                                        // 2 = 4-word unit, 3 = 8-word unit
};

struct TSN19T_4
{
    unsigned short        verifierh6:6;   // content verifier (hi bits)
    unsigned short        tsn16:1;        // TSN is 16 digits long (= 0 for TSN19)
    unsigned short        day9:9;         // meeting day/transaction day/draw number
};

struct TSN19_5
{
    unsigned short        unused4:4;
    unsigned short        verifierl12:12; // content verifier (lo bits)
};


struct TSN_SB           // soccer betting tsn
{
  struct TSN_SB1        w1;     // word 1
  unsigned short        reclwu; // word 2 - low order record offset bits
  struct TSN_SB3        w3;     // word 3
  struct TSN_4          w4;     // word 4
};

struct  TSN_4           //4th word of tsn
  {
  unsigned short  secu3:3;        //high order security code bits
                                //or presale day count in bet file
  unsigned short  sys3:3;         //sale system #
  unsigned short  new1:1;         //new tsn flag
  unsigned short  day9:9;         //meeting day of year [racing]
                                //draw # [lottery] or transaction day of year
  };

struct TSN_SB3                  // word 3 of soccer betting tsn
{
  unsigned short          ctr14:14;       // selling centre
  unsigned short          offUnit2:2;     // offset unit
                                // 0 = word unit, 1 = 2-word unit,
                                // 2 = 4-word unit, 3 = 8-word unit
        //  0 => rec from 0           to 0x3FFFFFF  (up to block 262143)
        //  1 => rec from 0x4000000   to 0xBFFFFFE  (up to block 786431)
        //  2 => rec from 0xC000000   to 0x1BFFFFFC (up to block 1835007)
        //  3 => rec from 0x1C0000000 to 0x3BFFFFF8 (up to block 3932159)
        // With this implemenation, we can store up to 16.77 million ticket per
        // day in soccer bet file.  This is calculated with average bet size 
        // equal to 120 bytes.
};


struct  TSN_SB1                 // word 1 of soccer betting tsn
  {
  unsigned short          rech10:10;      // high order bits of record offset
  unsigned short          yr1:1;          // last bit of sale year
  unsigned short          type3:3;        // bet type
    #define TSN_TYPE_SB         4       // soccer betting [w4.sys3=0
                                        // and w4.new1=1]
  unsigned short          secu2:2;        // low order bits of security code
  };

struct  TSN_A           //full tsn
  {
  struct TSN_12 w12;    // word 1 and 2
  union TSN_3   w3;     // word 3
  struct TSN_4  w4;     // word 4
  };

struct  TSN_4           //4th word of tsn
  {
  unsigned short  secu3:3;        //high order security code bits
                                //or presale day count in bet file
  unsigned short  sys3:3;         //sale system #
  unsigned short  new1:1;         //new tsn flag
  unsigned short  day9:9;         //meeting day of year [racing]
                                //draw # [lottery] or transaction day of year
  };  

struct  TSN_12          // word 1 and 2 of tsn
  {
  unsigned char         rechb;          // high order bits of record #
  unsigned char          loc3:3;         // location for racing ticket
    #define TSN_LOC_CV_ODDYR    1
    #define TSN_LOC_MK6         5
    #define TSN_LOC_SWP         6
    #define TSN_LOC_PWB         7
  unsigned char          type3:3;        // bet type
    #define TSN_TYPE_ESC        0
    #define TSN_TYPE_LOT        1       //single-draw lottery
    #define TSN_TYPE_AUP        2
    #define TSN_TYPE_EXO        3
    #define TSN_TYPE_STD        4
    #define TSN_TYPE_TBD        5
    #define TSN_TYPE_CV         6
    #define TSN_TYPE_MD         7       //multi-draw lottery
  unsigned char          secu2:2;        // low order bits of security code
  unsigned short        reclw;          // low order record # bits
  };

union   TSN_3                   // word 3
  {
  struct TSN_3OLD       old;    // old [w4.new1=0]
  struct TSN_3CTRWDW    ctrwdw; // centre/window
  };
// ..PN02

struct  TSN_3OLD                // old word 3
  {
  unsigned short  ctrl8:8;        //centre/eft low order bits
  unsigned short  wdw6:6;         //window [eft=0]
  unsigned short  ctrh2:2;        //centre/eft high order bits
  };

struct TSN_3CTRWDW
{
  unsigned short  ctrl10:10;      // centre number
  unsigned short  wdw6:6;         // window number
};


struct SBLOG_BET_ERR         // selling reject error info.          LY08
{
    unsigned char           poolbu;     // pool type
//ben    struct  SB_MATCH_ID     id;         // match ID
// ben add the following unsigned char
    unsigned char         daybu;                    // day of week
    unsigned char         matchbu;                  // match # within day
    unsigned short          selwu[2];   // selection                LY08
	unsigned int		  minibetval;
	unsigned char           levbu;      // the aup level number of reject max bet       // JC31
};



#define LOGAB_TRMREQ_MAX    512  
struct LOGAB_ILL                // illegal code
{
  unsigned char     codebu;                     // request code
  unsigned short    sizewu;                     // size of data
  char              datab[LOGAB_TRMREQ_MAX];    // request data
};



struct LOGAB_TXNENQ
{
    char                termtypeb;
    unsigned short      tranwu;
	LONGLONG			tokend;	// token of the retrieved transaction
    unsigned short      lenwu;
    char                bufb[512];
};



struct LOGAB_RELTRM         // Release Terminal
{
    struct AA_BCS_RELTERMREQ    req;        // Release Terminal request
    // following is filled in by BTHNDR
    int                         ltnl;       // logical terminal # of BT (-1 => no such terminal)
    unsigned int                stafflu;    // staff on released terminal
    LONGLONG                    bankgd;     // bank guarentee
    LONGLONG                    curDivd;    // unsettled dividend
    LONGLONG                    sbPFtd;     // soccer fo payout forfeited
    struct ACU_TRAN_ACR         tran;       // fund available at time of release
    LONGLONG                    divBal;     // Dividend pocket balance for IBT anonymous a/c (in cents) 2011IBT
};

struct ACU_TRAN_ACR
{
  LONGLONG      fundd;    // funds available
};

#define AA_TERMID_LEN       8
struct AA_BCS_RELTERMREQ
{
    char                termidb[AA_TERMID_LEN];    // Terminal ID
};


struct LOGAB_ACCBAL             // account balance via EFT, PAN capture
{
  struct LOGAB_PANCAP       pancap;
  struct LOGAB_EPS_EFT      eft;                                    // EH07
  unsigned char             chanbu;     // eft chanel #             // EH07
  unsigned int              gtwmsnlu;   // gateway msn
};

struct LOGAB_PANCAP
{
  unsigned char  typebu;                // pan type
  char           pans[ACU_PAN_SIZE];    // pan
};

struct LOGAB_EPS_EFT            // account related info in eft tran
{
  unsigned int          seculu;     // security code
  unsigned char         esc1:1;     // ESC EFT transaction
  struct ACU_TRAN_ACA   aca;        // account access information
};


struct LOGAB_CVI                // CV issue via EFT
{
  unsigned int          amountlu;       // amount in cents
  struct LOGAB_EPS_EGW  eps;                                        // EH07
};

struct LOGAB_EPS_EGW            // gateway information
{
  unsigned int          gtwmsnlu;                   // eft channel msn
  unsigned short        psuedowu;                   // EPSCO psuedo channel #
  unsigned short        epsretwu;                   // EPSCO return code
  unsigned short        eftSizewu;                  // size of eft portion
  unsigned char         chanbu;                     // eft channel #
  unsigned char         subCodebu;                  // eft sub-code from terminal
  unsigned char			eftPinbu:1;					// eft pin		-- Q405
  unsigned char			DESFlagbu:1;				// 3DES Flag	-- Q107
  unsigned char			reqfromchannel:1;			// Q210 request from channel
  unsigned char			regnocapture:1;				// registration number to be captured
  unsigned char			indnba:1;					// indicate bacnk number below is NBA
  unsigned char			chipcard1:1;				// indicate EMV Chip card
  unsigned char			fallback1:1;				// indicate EMV fallback
  unsigned char			reversal1:1;				// indicate EMV reversal
  unsigned char			eftFlagbu;					// eft flag		-- Q405 1 - bank pin, 2 - ATM pin
  char					eftAccNo[12];				// eft account no. -- Q405
  char                  isnb[6];                    // ISN
  unsigned char			nbano;						// NBA # 1=Pri, 2=Sec Q210

  char                  banks[ACU_BANK_SIZE+1];     // bank code
  char                  nbab[ACU_BANK_ACN_SIZE];    // nominated bank acc #
  int32_t				acttime;					// filler
  char                  eftb[LOGAB_EFTMSG_MAX];     // variable eft request/reply
};

struct LOGAB_EFT_LTEST      // link test request on EFT channel
{
  unsigned char     chanbu;
  unsigned int      gtwmsnlu;
};

struct LOGAB_EFT_MISC           // miscellaneous EFT activity
{
// unsigned char                 nbano;      // NBA number 1=pri, 2=sec
//  unsigned char         regno1:1;      // registration number to be captured
  struct LOGAB_EPS_CIT   cit;
  struct LOGAB_EPS_EGW   eps;                                       // EH07
};

struct LOGAB_ECVCLSENQ      // ECV close enquiry
{
  unsigned LONGLONG         escdu;              // esc card #
  unsigned char             accStatusbu;        // account status
  unsigned int              outstand1:1;        // outstanding transaction flag
  struct LOGAB_ADTLENQ      enq;                // account detail enquiry
};

struct LOGAB_ECVRET         // ECV return
{
  unsigned LONGLONG         escdu;              // esc card #
  unsigned LONGLONG         wtwAmtdu;           // withdrawal amount
  unsigned int              depRfdlu;           // deposit refund amount
  unsigned char             wtwTypebu;          // withdrawal type
  char                      cusidb[20];         // customer id.
  char                      reasons[30+1];      // reason
  unsigned int              fordep1:1;          // forfeit deposit flag [0=no forfeit]
  struct ACU_TRAN_ACA       tran;
  struct LOGBCSAA           bcs;                // bcs info
  struct AA_BCS_ECVCARDCANRPY   rpy;            // reply
};

struct LOGAB_ECVISS         // ECV issue
{
  unsigned LONGLONG         escdu;              // ECV card #
  unsigned LONGLONG         depAmtdu;           // deposit amount for opening balance
  unsigned char             accTypebu;          // account type (0=named account,1=anonymous)
  unsigned char             langbu;             // language (see acudef.h)
  char                      cusidb[20];         // customer id.
  char                      surnames[20+1];     // surname
  char                      othnames[40+1];     // other name
  char                      addrs[120+1];       // address
  char                      phones[2][20+1];    // phone #
  char                      sexb;               // 'F' / 'M'
  char                      locationb;          // location
  unsigned int              wavflg1:1;          // waive card deposit fee flag
  struct BCS_DATE           dob;                // date of birth
  struct LOGBCSAA           bcs;                // bcs info
  struct AA_BCS_ECVCARDISSRPY   rpy;            // reply
};

struct AA_BCS_ECVCARDISSRPY
{
    unsigned int        accnumlu;    // Account number
    unsigned int        depfeelu;    // Deposit Fee (in cents)
    unsigned int        seccodelu;   // Security code

};

struct LOGAB_DEVCAN         // device cancel
{
  unsigned char                 devbu;      // device type, check DEV_TYP
  unsigned char                  ver1:1;  // Q309 version - Q210 
  unsigned LONGLONG             devdu;      // device #
  unsigned char                  fordep1:1;  // forfeit deposit
  unsigned char                  :7;         // unused
  struct ACU_TRAN_ACA           tran;
  struct LOGBCSAA               bcs;        // bcs info
  struct AA_BCS_DEVCANRPY       rpy;        // reply
};

struct AA_BCS_DEVCANRPY
{
    unsigned int        annlfeereflu;   // Annual fee refund (in cents)
    unsigned int        depfeelreflu;   // Deposit fee refund (in cents)
};

struct LOGAB_DEVREPL        // device replace
{
  unsigned int                  seculu;     // security code
  unsigned char                 olddevbu;   // old device type, check DEV_TYP
  unsigned char                  olddevver1:1;  // old device Q309 version
  unsigned LONGLONG             olddevdu;   // old device #
  unsigned char                 newdevbu;   // new device type, check DEV_TYP
  unsigned char                  newdevver1:1;  // old device Q309 version
  unsigned LONGLONG             newdevdu;   // new device #
  unsigned char                 newverbu;   // new cit version (ascii)
  unsigned char                  upddep1:1;  // update deposit
  unsigned char                  fordep1:1;  // forfeit deposit
  unsigned char                  versecu1:1; // verify security code
  unsigned char                  :5;         // unused
  struct ACU_TRAN_ACA           tran;
  struct LOGBCSAA               bcs;        // bcs info
  struct AA_BCS_DEVREPRPY       rpy;        // reply
};

struct LOGAB_DEVISS         // device issue
{
  unsigned int                  seculu;     // security code
  unsigned char                 devbu;      // device type, check DEV_TYP

  unsigned char                 ver1:1;  // Q210 - Q309 version 
  
  unsigned LONGLONG             devdu;      // device #
  unsigned char                 verbu;      // cit version (ascii)
  struct ACU_TRAN_ACA           tran;
  struct LOGBCSAA               bcs;        // bcs info
  struct AA_BCS_DEVISSUERPY     rpy;        // reply
};

// reply (BCS->OLTP)
struct AA_BCS_DEVISSUERPY
{
    unsigned int        annlfeededlu;   // Annual fee deduction (in cents)
    unsigned int        depfeededlu;    // Deposit fee deduction (in cents)
};


struct LOGAB_AUTHVER        // authority verification 
{
  unsigned int      stafflu;            // staff to verify
  unsigned int      passwordlu;         // password
  unsigned char     pwdLenbu;           // password length
  unsigned char     funcCodebu;         // function code
    #define AUTHVER_CODE_BET_SELL     1     // large bet selling
  struct LOGBCSAA   bcs;                // bcs info
};

struct LOGAB_CHGSCD         // bt charge security code
{
  char                      cusidb[20];     // customer id.
  unsigned int              oldSeculu;      // old security code
  unsigned int              newSeculu;      // new security code
  struct LOGBCSAA           bcs;            // bcs info
  struct AA_BCS_CHGSECRPY   rpy;            // reply
};

struct AA_BCS_CHGSECRPY
{
    unsigned char       lockVBTbu;     // 0 = FALSE, otherwise TRUE
};


struct LOGAB_CARDRET        // return esc card
{
  char                      cusidb[20];     // customer id.
  unsigned char             fordep1:1;      // forfeit deposit flag [0=no forfeit]
  unsigned LONGLONG         escdu;          // esc card #
  struct LOGBCSAA           bcs;            // bcs info
  struct AA_BCS_DEVCANRPY   rpy;            // reply
};

struct LOGAB_CARDREPL       // replace esc card
{
  unsigned LONGLONG             oldEscdu;   // old esc card #
  unsigned LONGLONG             newEscdu;   // new esc card number
  char                          cusidb[20]; // customer id.
  unsigned int                  seculu;     // security code
  unsigned char                 fordep1:1;  // forfeit deposit flag [0=no forfeit]
  unsigned char                 wavdep1:1;  // wavie deposit flag [0=not waive]
  struct ACU_TRAN_ACA           tran;
  struct LOGBCSAA               bcs;        // bcs info
  struct AA_BCS_DEVREPRPY       rpy;        // reply
};

struct LOGAB_CARDISS        // issue esc card
{
  char                          cusidb[20]; // customer id
  unsigned int                  seculu;     // security code
  unsigned char                 wavflg1:1;  // waive card deposit fee flag
  unsigned char                 withHold1:1;  // witholdable
  unsigned char                 :6;			  // unused
  int32_t						reltime;
  unsigned LONGLONG             escdu;      // esc card #
  unsigned LONGLONG             depAmtdu;   // deposit amount
  struct ACU_TRAN_ACA           tran;
  struct LOGBCSAA               bcs;        // bcs info
  struct AA_BCS_DEVISSUERPY     rpy;        // reply
};

struct LOGAB_ADTLENQ        // account detail enquiry
{
  unsigned char             reqtypebu;  // request type
    #define ADTLENQ_ID      1           // id
    #define ADTLENQ_SEXNAME 2           // sex and name
    #define ADTLENQ_ECVFEE  3           // ECV deposit fee
  struct LOGBCSAA           bcs;        // bcs info
  union AA_BCS_ACCDETRPY    rpy;        // BCS-AA reply
};

union AA_BCS_ACCDETRPY
{
    struct AA_BCS_HKID  hkid;       // HK ID
    struct AA_BCS_SEX   sex;        // Sex
    struct AA_BCS_DEVDEPFEE devdepfee; // KL33, Device Deposit Fee
};

#define AA_HKID_LEN         21
struct AA_BCS_HKID
{
    char                hkids[AA_HKID_LEN];   // HK ID
};

#define AA_SURNAME_LEN      21
#define AA_OTHNAME_LEN      41
#define AA_CHNSURNAME_LEN   12
#define AA_CHNOTHNAME_LEN   12
#define AA_HKID_LEN         21

struct AA_BCS_SEX
{
    char                sexb;        // Sex, 'F'/'M'
        #define FEL     'F'          // Female
        #define MAL     'M'          // Male
    char                surnames[AA_SURNAME_LEN];
    char                othernames[AA_OTHNAME_LEN];
    char                chinsurnames[AA_CHNSURNAME_LEN];
    char                chinothnames[AA_CHNOTHNAME_LEN];
};

struct AA_BCS_DEVDEPFEE
{
    unsigned int        amountlu;    // Device Deposit Fee (in cents)
};



union LOGAB_SB
{
  struct LOGAB_SBMSG   msg;         // terminal message
  struct LOGAB_SBBET   bet;         // reply
};

struct LOGAB_SBMSG
{
  unsigned int		minTktTot;                   // Q310 Minimun Ticket Total 
  unsigned short        lenwu;                      // terminal data length
  unsigned char         trmDatabu[450];  // terminal data [variable]
};

struct LOGAB_RCL
{
  unsigned char         typebu;     // recall type
    #define LOGAB_RCL_START   1     // recall start - no specific data
    #define LOGAB_RCL_CON     2     // recall continue
    #define LOGAB_RSTA_STA    3     // statement start
    #define LOGAB_RSTA_CON    4     // statement continue
  union LOGAB_RCL_DATA  data;       // request specific data
  //struct LOGAB_RCL_INF  start;      // points to start of current recall, (Removed from 201108PSR)
};

union LOGAB_RCL_DATA            // request specific recall data
{
  struct LOGAB_RCL_STA  rstaSta;    // statement start
  struct LOGAB_RCL_INF  rstaCon;    // statement continue
  struct LOGAB_RCL_TXN  rstaTxn;	// Recall transaction (Added 201108PSR)
  //unsigned short        tranwu;     // transaction number - recall continue (Removed from 201108PSR)
};

struct LOGAB_RCL_STA
{
  int32_t                date;       // date - statement start
  unsigned int          acclu;      // account #
  unsigned int          trnbitmap;  // Transaction Filter Bitmap (Added 201108PSR)  (No Decode Yet)
};

struct LOGAB_RCL_INF
{
  unsigned int          blocklu;    // block #
  unsigned short        blkOffwu;   // block offset
  unsigned short        trnOffwu;   // transaction offset
  unsigned short        filewu;     // file #
  unsigned int          trnbitmap;  // Transaction Filter Bitmap (Added 201108PSR)  (No Decode Yet)
};

struct LOGAB_RCL_TXN  //Recall transaction (Added 201108PSR)
{
  unsigned short        tranwu;   // Transaction number
  unsigned int          token;   // Continuation token
};

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

union LOGAB_CAN_DATA
{
  struct LOGAB_LOT    lot;
  struct LOGAB_RAC    rac;
  struct LOGAB_WTW    wtw;
  union  LOGAB_SB     sb;
  struct LOGAB_DEP    dep;
};

struct LOGAB_DEP
{
  struct ACU_TRAN_DEP   tran;       // transaction in account file
  union LOGAB_DEP_DATA  data;       // deposit detail
};

union LOGAB_DEP_DATA
{
  struct LOGAB_EPS_TB   eps;        // epsco info.
  struct LOGAB_TB_DEP   tb;
  struct LOGAB_FPS		fps;		//FPS
};

struct LOGAB_TB_DEP
{
  union TSN             tsn;        // TSN
  struct ACU_TRAN_ACA   aca;        // account access information    
};


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

struct LOGAB_WTW
{   
  struct ACU_TRAN_WTW   tran;       // withdrawal transaction in account file
  union {
	  struct LOGAB_EPS_TB   eps;      // eps information                 // EH07
	  struct LOGAB_FPS		fps;		// FPS
	  unsigned int			divprocddtlu;  // Amount in dollar deducted from dividend pocket;0=normal a/c> 0 for IBT anonymous a / c only
  };
};

struct LOGAB_FPS
{
	struct ACU_TRAN_ACA aca;
	struct LOGAB_FPS_INFO fpsinf;
};

struct ACU_TRAN_ACA
{
  LONGLONG      fundd;    // funds available
  //LONGLONG      bankgd;   // bank guarentee
  LONGLONG		dpflag1 : 1;// bankgd stores dividend pocket (DP) instead of BG   // JC50
  LONGLONG		cscflag1 : 1;// CSC account access                                // CS52
  LONGLONG		ewalletflag1 : 1;// eWallet account access						  //SP21a
  LONGLONG		reserved : 13;                                                    // JC50
  LONGLONG      bankgd : 48;// bank guarentee (BG) or settled divdend pocket (DP) // JC50
  LONGLONG      curDivd;  // unsettled dividend
  LONGLONG      prvDivd;  // previous dividend
  LONGLONG      sbPFtd;   // soccer fo payout forfeited
};

struct LOGAB_FPS_INFO
{
	unsigned int		fpsgwsysid;			//FPS gateway system ID
	LONGLONG			refno;				//Reference No.
	unsigned int		fpsprocessid;		//FPS process ID
	unsigned int		channelid;			//Channel ID
	//char				custname[256];	    //CustomerName
	char				nbano;				//NBA #, 1=primary, 2=secondary
	char				bankcode[4];		//Bank Code
	char				nombankacc[26];		//Nominated bank acc #
	char				actiontype;			//Action, 1=Request, 2=Undo
	char				jsonMsg[700];		//Request message(JSON) from FPS gateway
};

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

struct ACU_TRAN_LOT2
{
  unsigned int     content;
  struct BETABLOT  bet;
};

struct BETABLOT
{
  unsigned char   srcbu:7;    // source of sell (Changed 201108PSR)
  unsigned char   csctrn:1;  // Transaction with CSC Card (Added 201108PSR)
  //unsigned short  yearwu;   // year
  //unsigned short  drawwu;   // draw #
  //unsigned short  typewu;   // type of lottery
  struct BETDATA  d;        // data
};

struct  BETDATA
{
  struct BETHDR         hdr;    // common header
  union BETVAR          var;    // variable part
};

union   BETVAR                          // variable part
{
  struct BETAUP         a;      // allup
  struct BETEXOSTD      es;     // exotic/standard
  struct BETLOT         lot;    // lottery
  struct BETDEP         cv;     // cash voucher
  struct BETSB_DET      sb;     // soccer betting
};

#define BET_AUP_MAXEVT   6          // max. event of allup
#define BET_BNKM_MAXLEG  3          // maximum leg for banker bit map
#define BET_MLP_MAXLEG   6          // maximum leg for multi leg pool
#define BET_RAC_MAXSMAP  2     

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

union BETEXBNK
{
  unsigned long long      sellu[BET_MLP_MAXLEG];  // selection bitmap
  unsigned char         bnkbu[BET_BNKM_MAXLEG]; // # of bankers per leg [max. 3 legs]
};

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

struct  BETAUP          // allup selections
{
  unsigned char			loc;			// location
  unsigned char			day;			// Day
  int32_t			md;				// meeting day
  unsigned char         evtbu;          // # of events
  unsigned char         fmlbu;          // formula
  struct BETAUPSEL      sel[BET_AUP_MAXEVT];    // selections
};

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

struct  BETHDR                          // common header
{
  unsigned LONGLONG     totdu;          // total payout in cents
  union BETINVESTCOMBO	betinvcomb;		// Q308 changes
  unsigned int     costlu;         // total cost in cents
  int32_t                sellTime;       // sell time
  unsigned int			businessDate;		// business date
  unsigned char         bettypebu;      // bet type
  struct BETSTS         sts;
};

struct BETSTS           // bet status
{
  unsigned short          cancel1:1;      // cancel
  unsigned short          paidpart1:1;    // paid - partial
  unsigned short          paidfinal1:1;   // paid - final
  unsigned short          divcal1:1;      // divcal - dividend is finalised
                                        // In sb system, this bit will
                                        // be set when all matches of 
                                        // involved can be concluded during
                                        // eod.  Cancelled "SB" bet is also set
                                        // with this bit too such that latest
                                        // match date in the bet can be updated
                                        // as reference in the period of bet
                                        // retention in system.
  unsigned short          claim1:1;       // error claimed
  unsigned short          released1:1;    // released to be paid at centre payCentrelu
  unsigned short          overflow1:1;    // overflow
  unsigned short          hop1:1;         // h.o. payment
  unsigned short          bonusovfl1:1;   // bonus overflow       FT03
  unsigned short          shrink1:1;      // bet shrunk to shrink bet file  RL04
                                        // For soccer betting system, this bit 
                                        // set implies that bet must be kept in
                                        // system until payout expires.  This
                                        // bet may exist in daily bet file or
                                        // shrink bet file.
  unsigned short          nsize1:1;       // new size for SB simple pool record
                                        // in order to fix wrong calculation
                                        // of selection size in parimutual
                                        // (for newly issued SB bet, this
                                        // bit will always be set)  PN16
  unsigned short          fieldsizef1 :1;  // Using 34 field size flag AUG2020, replace extot1
  unsigned short		  forfeitfl:1;  // Q405 Forfeit flag - If this flag is set before dividend 
  unsigned short          lscovfl1:1;     // losing inv. consolation overflow
  unsigned short          :2;             // for future expansion DD02 FT03 RL04
};

union BETINVESTCOMBO
{
	//unsigned int	baseinv:31;	// flexibet=0; BASE investment in dollar; flexibet = 1; noofcombination
	//unsigned int	flexibet:1;	// flexi bet	
	struct BETFLEXICOMBO flexi;

	unsigned int    binvlu;         // base investment in dollar. added by in sp3. 2016.10.20
};

struct BETFLEXICOMBO
{
	unsigned int	baseinv:31;	// flexibet=0; BASE investment in dollar; flexibet = 1; noofcombination
	unsigned int	flexibet:1;	// flexi bet	
};

struct LOGAB_RAC
{
  union LOGABRAC_BET_INFO betinfo;
  unsigned short        indexwu;    // meeting index
  unsigned char			crossSellFl:1; // cross sell indicator
  unsigned char			:7;
  struct ACU_TRAN_RAC2   tran;
};

struct ACU_TRAN_RAC2
{
  unsigned int     content;
  struct BETABRAC  bet;
};

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


union LOGABRAC_BET_INFO
{
	struct LOGABRAC_BET_UPD		raceinfo;   // Race Sell Bet info (2011IBT Changes)
	struct LOGABRAC_BET_ERR		errorinfo;	// error info  
};

struct LOGABRAC_BET_UPD
{
	unsigned int				offsetlu;   //offset of bet in file		
	unsigned int				tranamt;    //Transferred amount (In cents) (201108PSR - changed from short to int)
};

struct LOGABRAC_BET_ERR
{
	unsigned int	   minbettot;      // Minimum bet total in cents on error "total min. investment not met"    
	unsigned char      racebu;     // error race number
    unsigned char      selbu;      // error selection
};


struct LOGAB_ACR                // account release
{
  unsigned short        keyStrokewu;    // key stroke count
  unsigned char         errStrokebu;    // error stroke count
  unsigned char         relcodbu;       // release code
    #define ACR_CODE_NONESC     0       // non ESC account release
    #define ACR_CODE_CRDRM      2       // initiated by terminal due to card removal
    #define ACR_CODE_EFTTO      3       // initiated by terminal due to timeout or unposted
    #define ACR_CODE_ATREL      4       // CB-AT requests the a/c release
    #define ACR_CODE_EMERG    100       // Emergency account release
  LONGLONG              bankgd;         // bank guarentee
  LONGLONG              curDivd;        // unsettled dividend
  LONGLONG              sbPFtd;         // soccer fo payout forfeited
  struct ACU_TRAN_ACR   tran;
  LONGLONG              divBal;     // Dividend pocket balance for IBT anonymous a/c (In cents <settle + unsettle>) 2011IBT
};

struct LOGAB_ACA
{
  unsigned char         reqfromchannel:1;  // Q210 request from channel
  union LOGAB_ACA_DEV   dev;            // device specific info.
  union LOGAB_ACA_DATA  data;
};

union LOGAB_ACA_DEV             // device info of account access
{
  struct LOGAB_ACA_VOICE    voice;
  struct LOGAB_ACA_DID      did;
  struct LOGAB_ACA_CB       cb;
  struct LOGAB_ACA_PINVER   pinver;  //Account PIN Verification (Added 201108PSR)
};

struct LOGAB_ACA_VOICE
{
  unsigned int          recTrklu;       // recorder track
  unsigned int          seculu;         // security code
  unsigned char          secu1:1;        // security code override
  unsigned char          :7;
};

struct LOGAB_ACA_DID
{
  unsigned char         citbu;          // device type, check DEV_TYP
  unsigned char          oth1:1;         // other cit
  unsigned char          :7;
  unsigned int          seculu;         // security code
};

struct LOGAB_ACA_CB
{
  unsigned LONGLONG     escdu;          // esc #
  unsigned short        rejcodwu;       // CMS reject code
  unsigned char          svt1:1;
  unsigned char          oncourse1:1;
  unsigned char          :6;
};

struct LOGAB_ACA_PINVER   //Account PIN Verification (Added 201108PSR)
{
  unsigned char          balreq:1;		//Bit 0 = Balance required for the reply to caller
  unsigned char          :7;			//Unused
  unsigned int           seculu;        //security code
};

union LOGAB_ACA_DATA
{
  struct LOGAB_SOURCE       busySrc;    // terminal accessing account for account active error
  struct LOGAB_ACA_NORMAL   normal;     // for okay or other error
};

struct LOGAB_SOURCE
{
  unsigned char             srcTypebu;  // source type
    #define LOGAB_SRC_VOICE      1     // voice
    #define LOGAB_SRC_CIT        2     // cit, use LOGAB_SOURCE_DID
    #define LOGAB_SRC_MAT        3     // mat
    #define LOGAB_SRC_CB_BT      4     // cb bt
    #define LOGAB_SRC_EWIN       5     // ewin, use LOGAB_SOURCE_DID
    #define LOGAB_SRC_OLD        6     // old protocol by channel and system
    #define LOGAB_SRC_BAT_DEP    7     // batch deposit - tb #
    #define LOGAB_SRC_EFT_CB     8     // eft from cb, use LOGAB_SOURCE_CBBT
    #define LOGAB_SRC_EFT_CIT    9     // eft from cit, use LOGAB_SOURCE_DID
    #define LOGAB_SRC_SBC       10    // soccer betting control
    #define LOGAB_SRC_AUTO      11    // system generated
    #define LOGAB_SRC_EOD       12    // eod generated
    #define LOGAB_SRC_WC        13    // wagering control
    #define LOGAB_SRC_POL       14    // pre-online
    #define LOGAB_SRC_OPR       15    // operator
    #define LOGAB_SRC_EFT_EWIN  16     // eft from ewin, use LOGAB_SOURCE_DID
    #define LOGAB_SRC_TBASD     17    //  TBASD Added Q407
    #define LOGAB_SRC_EFT_TBASD 18    // TBASD Added Q407
	#define LOGAB_SRC_CB_EWAL   19    // eWallet added for SP21a
	#define LOGAB_SRC_EFT_FPS   20    // FPS added for SP21a
	#define LOGAB_SRC_MAX       29    // max type
  union LOGAB_SOURCE_DATA   data;
};

union LOGAB_SOURCE_DATA
{
  struct LOGAB_SOURCE_VOICE  voice;
  struct LOGAB_SOURCE_DID    did;
  unsigned int               matlu;
  struct LOGAB_SOURCE_CBBT   cbBt;
  struct LOGAB_SOURCE_OLD    old;
  unsigned short             tbwu;  // batch deposit
  struct LOGAB_SOURCE_POL    pol;
};

struct LOGAB_SOURCE_VOICE
{
  unsigned char   febu;    // frontend #
  unsigned short  termwu;  // terminal #
  unsigned int    locidlu; // location id
  unsigned char train1 : 1;     // training mode flag RL64
};
struct LOGAB_SOURCE_DID
{
 unsigned int    citlu;     // cit #
  unsigned char   termbu;    // pseudo terminal #
  unsigned char   febu;      // frontend #
  unsigned char   citTypebu; // cit type
};
struct LOGAB_SOURCE_CBBT
{
  //unsigned int    centrelu; 
  unsigned int    centrelu:24;  // centre number (Changed 201108PSR)
  unsigned int    csctrn:1;     // Transaction with CSC Card  (Added 201108PSR)
  unsigned int    ewallettrn : 1;     // eWallet for SP21a
  unsigned int    unused:6;		// Unused  (Added 201108PSR)
  unsigned short  windowwu;  // window number
  unsigned short  ltnwu;     // logical terminal #
  unsigned char   cbbu;      // cb system #
};
struct LOGAB_SOURCE_OLD
{
  unsigned int    centrelu;  // centre number
  unsigned short  windowwu;  // window number
  unsigned short  chanwu;    // channel #
  unsigned char   cbbu;      // cb system #
};
struct LOGAB_SOURCE_POL
{
  unsigned char   filebu;    // file number
  unsigned int    offsetlu;  // offsetlu;
  unsigned int    skpAca1:1; // no auto acc. access generation flag
};

struct LOGAB_SGF                // sign-off
{
  struct LOGBCSAA   bcs;            // bcs info
};

struct LOGAB_SGN                // sign-on
{
  unsigned int              passwordlu;         // password
  unsigned char             pwdLenbu;           // password length
  struct LOGBCSAA           bcs;                // bcs info
  struct AA_BCS_BTSGNRPY    rpy;                // bcs reply
};

struct LOGBCSAA                 // BCS-AA system information
{
  unsigned char          disable1:1;     // bcs service is disabled
  unsigned char          :7;             // unused
};

struct AA_BCS_BTSGNRPY
{
    unsigned int        rectrklu;      // Recorder track
    struct AA_BCS_BTSGNAUTH auth;      // authority bitmap
};

struct AA_BCS_BTSGNAUTH
{
    unsigned int        secu1:1;        // Security code override
    unsigned int        super1:1;       // Super key account access
    unsigned int        key1:1;         // Key account access
    unsigned int        normal1:1;      // Normal account access
    unsigned int        fb9acc1:1;      // FB Type 9 A/C Access
    unsigned int        signon1:1;      // Sign on
    unsigned int        signoff1:1;     // Sign off
    unsigned int        racesell1:1;    // Race bet selling
    unsigned int        lotsell1:1;     // Lottery bet selling
    unsigned int        fbsell1:1;      // FB bet selling
    unsigned int        cheqwtd1:1;     // Cheque withdrawal
    unsigned int        aupaywtd1:1;    // Autopay withdrawal
    unsigned int        cancurcall1:1;  // Cancel current call bets
    unsigned int        canprvcall1:1;  // Cancel previous call bets
    unsigned int        reccurcall1:1;  // Recall current call bets
    unsigned int        recprvcall1:1;  // Recall previous call bets
    unsigned int        hvbetauth1:1;   // High value bet authorization
    unsigned int        :15;            // not used
};

union LOGAB_POL             // pre-online general
{
  struct LOGAB_POL_CKP     ckp;     // pre-online checkpoint request
  struct LOGAB_POL_BG      bg;      // pre-online bank guarantee
  struct LOGAB_POL_CHGSTS  sts;     // pre-online change account status
  struct LOGAB_SILOT_ACA   lotaca;  // pre-online account access
  struct LOGAB_SILOT       lot;     // pre-online s.i. lottery post
  struct LOGAB_SIWTW       wtw;     // pre-online s.i. withdrawal
  struct LOGAB_LOYALTY     loyalty; // loyalty device fee refund/deduction
  struct LOGAB_ACR         acr;     // pre-online account release
  struct LOGAB_POL_DETCDT  detcdt;  // debit/credit adjustment
};

struct LOGAB_POL_DETCDT     // pre-online debit/credit adjustment
{
  struct ACU_TRAN_ACA   aca;        // fill in by BTHNDR
  struct ABPOL_DCR_ADJ  data;       // debit/credit adjustment request
};

#define ABPOL_TXT_MAX       512   
struct ABPOL_DCR_ADJ            // debit credit adjustmen
{
    unsigned LONGLONG   amountdu;       // amount
    unsigned int        typelu;         // Adjustment Type 
    BOOL                negbalb;        // TRUE = allow negative balance
    char                remarks[ABPOL_TXT_MAX+1];   // remark variable length
};

struct LOGAB_ACR                // account release
{
  unsigned short        keyStrokewu;    // key stroke count
  unsigned char         errStrokebu;    // error stroke count
  unsigned char         relcodbu;       // release code
    #define ACR_CODE_NONESC     0       // non ESC account release
    #define ACR_CODE_CRDRM      2       // initiated by terminal due to card removal
    #define ACR_CODE_EFTTO      3       // initiated by terminal due to timeout or unposted
    #define ACR_CODE_ATREL      4       // CB-AT requests the a/c release
    #define ACR_CODE_EMERG    100       // Emergency account release
  LONGLONG              bankgd;         // bank guarentee
  LONGLONG              curDivd;        // unsettled dividend
  LONGLONG              sbPFtd;         // soccer fo payout forfeited
  struct ACU_TRAN_ACR   tran;
  LONGLONG              divBal;     // Dividend pocket balance for IBT anonymous a/c (In cents <settle + unsettle>) 2011IBT
};



struct LOGAB_LOYALTY        // CMS (loyality system)
{
  struct ACU_TRAN_ACA   aca;        // fill in by BTHNDR
  unsigned char          negbal1:1;  // cause negative balance flag
  struct ABPOL_LOYALTY  data;       // fee refund/deduction

};

struct ABPOL_LOYALTY            // Work records generated by Loyalty 
{
    unsigned LONGLONG   amountdu;       // amount
    unsigned LONGLONG   citdu;          // cit # or esc #
    unsigned char       cittypbu;       // CIT Type
    char                remarks[ABPOL_TXT_MAX+1];
};

struct LOGAB_SILOT          // pre-online s.i. lottery post
{
  unsigned int          siEntrylu;  // SI entry number
  unsigned char         lotTypebu;  // lottery type
  int32_t                drawdate;   // lottery draw date
  struct LOGAB_LOT      lot;        // lottery details
};

struct ABPOL_LOTACA             // lottery S.I account access
{
    BOOL                succt;          // Successful Flag
    BOOL                ndrawt;         // n-Draw Failure Flag
    unsigned int        ttlAmtlu;       // batch total amount
    unsigned int        countlu;        // Total No. of Mark 6 SI Count   
    unsigned char       lotTypebu;      // lottery type MK6/GBL
};

struct LOGAB_SILOT_ACA      // pre-online account access
{
  struct ABPOL_LOTACA   lot;        // check information
  int32_t                drawdate;   // lottery draw date
  union LOGAB_ACA_DATA  data;
};

struct LOGAB_POL_CHGSTS     // pre-online change account status
{
  struct ABPOL_STS      chg;
  struct ACU_TRAN_ACA   tran;       // Account Balance
};

struct ABPOL_STS                // change account status
{
    unsigned char       oldStatusbu;    // old status, see ACUDEF.H, ACU_STATUS_...
    unsigned char       newStatusbu;    // new status, see ACUDEF.H, ACU_STATUS_...
};


struct LOGAB_POL_BG         // pre-online bank guarantee
{
  struct ABPOL_BG       oldBg;      // old bank guarantee information
  struct ABPOL_BG       newBg;      // new bank guarantee information
};

struct ABPOL_BG                 // change bg request
{
    LONGLONG            bankgd;         // bank guarantee
    unsigned char       bgTypebu;       // bank gaurantee type
};

struct LOGAB_POL_CKP        // pre-online checkpoint request
{
  struct ABPOL_STATUS   oldStatus;   // old pre-online status
  struct ABPOL_CKP      status;      // new pre-online status
};

struct ABPOL_CKP                // pre-online done, checkpoint
{
    struct ABPOL_STATUS status;          // pre-online service status
    BOOL                sodt;            // pre-online all service done
};

struct ABPOL_STATUS             // pre-online service status
{
    enum POL_JOB_STS    jobsta[POLJOB_MAX];
    unsigned char        start1:1;       // receive start pol-online
    unsigned char        cvtdone1:1;     // file convert done
    unsigned char        postdone1:1;    // all job done
    unsigned char        :5;
};

enum POL_JOB_STS
{
    POL_STS_PENDING = 0,
    POL_STS_DOING,
    POL_STS_BYPASSED,
    POL_STS_DONE,    
};

union LOGOTH
{
    struct LOGOTHSRV     service;
    struct LOGOTHAPS     auppss;
    struct LOGOTHLWPS    lotwpss;
    struct LOGOTHEFTGW   eftgw;
    struct LOGOTHSYSCLS  syscls;    // RL02
};

struct  LOGOTHSRV               // enable / disable service
{
    unsigned short syswu;       // system number of corresponding system
    unsigned short bupsyswu;    // back up system number for bcs when it is
                                // disabled
    unsigned char enable1:1;   // enable flag
    unsigned char :7;          // unused
};

struct LOGOTHAPS                // allup pass done record
{
    unsigned short indexwu;     // meeting index
    unsigned short racewu;      // race number
};


#define LOT_MAXGAME 10  // # of games per draw
struct LOGOTHLWPS               // lotter winner pass record
{
    unsigned short lotidxwu;    // lottery index in lotcom
    unsigned short bfcidxwu;    // lottery index in bfccom
    unsigned LONGLONG nxtinvdu[LOT_MAXGAME];
                                // collations
};

struct LOGOTHEFTGW              // change EFTGW
{
  unsigned char sysbu;          // system to use (1 or 2)
};

// RL02..
struct LOGOTHSYSCLS             // system close
{
    unsigned short  clsenq1:1;      // system close for enquiry
};

union EODTRN_LOG            // tran that have to be logged
{
    struct EODTRN_DIV_PUR     divpur;       // dividend purged for SB upto Q106
    struct EODTRN_DIV_PUR2    divpur2;      // dividend purged after Q206
    struct EODTRN_DFT         dft;          // dividend forfeited
    struct EODTRN_DRCR        drcr;         // dr/cr transaction
                                            //  for typelu=ACU_CREDIT_BGRIM only
    // FT07...
    struct EODTRN_LOT         lot;          // cancel m6 s.i.; LOT div post 
    struct EODTRN_SB          sb;           // SB div post
    struct EODTRN_HSTRAC2     rac2;         // RAC2 div post
    // ...FT07
    struct EODTRN_LOT2         lot2;          // cancel m6 s.i.; LOT div post 
    struct EODTRN_SB2          sb2;           // SB div post
    struct EODTRN_HSTRAC3      rac3;         // RAC3 div post
};

struct EODTRN_HSTRAC3       // RAC3 tran in history file
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_HSTRAC3 body;
    union EODTRN_END        end;        // since struct BETDATA is of
                                        // variable size, EODTRN_END may be
                                        // put at variable position        
};

union EODTRN_END
{
    unsigned short          sizewu;     // for settled tran
    struct EODTRN_EXTRA     ext;        // for unsettled tran
};

struct EODTRN_EXTRA
{
    struct ACU_TRAN_EXTRA   e;
    unsigned short          sizewu;
};

struct ACU_TRAN_EXTRA       // extra info for unsettled transaction in
{                           // transaction file
  unsigned char   histFilebu;   // history file number
  unsigned int    histOfflu;    // offset to transaction in history file
  unsigned int    acaOfflu;     // offset of last a/c access in hist file !FT11
};

struct ACU_TRAN_HSTRAC3
{
	unsigned int			   content;
    struct BETABRAC2           rac2;
};

struct BETABRAC2                // for AB history & DIVBET only
{
    struct BETABEXTRA   extra;
    struct BETABRAC     bet;
};

struct BETABEXTRA
{
  unsigned short   lenwu;
  unsigned int     lscnlu;      // losing consolation in cents     
                                // only available when final paid or div cal bit is set.  
  // more attributes can be added here in future
};

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

struct ACU_TRAN_HDR
{
  unsigned short  sizewu;  // size of transaction
                           // transaction ends with size field
  unsigned short  codewu;  // transaction code, pls update acudatvar.h as well
    #define ACU_CODE_LOT         1  // lottery
    #define ACU_CODE_RAC         2  // racing
    #define ACU_CODE_WTW         3  // withdrawal
    #define ACU_CODE_CAN         4  // cancel
    #define ACU_CODE_SB          5  // soccer bet
    #define ACU_CODE_ACA_CB      6  // CB account access
    #define ACU_CODE_ACA_VOICE   7  // voice account access
    #define ACU_CODE_ACA_CIT     8  // cit account access
    #define ACU_CODE_ACA_MAT     9  // MAT account access
    #define ACU_CODE_ACA_AUTO   10  // auto account access
    #define ACU_CODE_CIT_DEP    11  // CIT/esc deposit
    #define ACU_CODE_CIT_DEPRFD 12  // cit/esc deposit refund
    #define ACU_CODE_CIT_FEE    13  // cit annual fee
    #define ACU_CODE_CIT_FEERFD 14  // cit annual fee refund
    #define ACU_CODE_DEP_TSN    15  // CB deposit with tsn, including payout deposit
    #define ACU_CODE_DEP_ATM    16  // Batch deposit
    #define ACU_CODE_DEP        17  // non-cash deposit [without tsn]
    #define ACU_CODE_HSTACC     18  // history account sod
    #define ACU_CODE_DEBIT      19  // debit adjustment
    #define ACU_CODE_CREDIT     20  // credit adjustment
    #define ACU_CODE_ACR        21  // account release
    #define ACU_CODE_SOD        22  // sod
    #define ACU_CODE_RIM        23  // bank guarantee reimbursement outstanding
    #define ACU_CODE_DIV        24  // dividend settled tonight
    #define ACU_CODE_DIV_PUR    25  // dividend of purged transaction
    #define ACU_CODE_LOT_SI     26  // unsatifised si lottery
    #define ACU_CODE_PANCAP     27  // PAN capture
                                    // same format as ACU_CODE_LOT
    #define ACU_CODE_DFT        28  // dividend forfeited       ! FT03
    #define ACU_CODE_AFR        29  // cit annual fee reverse   ! FT03
    #define ACU_CODE_CHARGE     30  // service charge
    #define ACU_CODE_DIV_OS     31  // dividend from o/s esc transaction
    #define ACU_CODE_STMCHG     32  // statement charge
    #define ACU_CODE_CIT_PDRFD  33  // progressive cit deposit refund !FT19
    #define ACU_CODE_OLDTB      34  // legacy system tranasction    PN20
    #define ACU_CODE_CIT_DEPFFT 35  // CIT/esc deposit forfeit
    #define ACU_CODE_HSTRAC2    36  // tran ACU_CODE_RAC in history file !FT27
                                    //      use structre ACU_TRAN_HSTRAC2
    #define ACU_CODE_DIV_PUR2   37  // purged transaction after Q206

	#define ACU_CODE_LOT2		38  // used by esc
	#define ACU_CODE_RAC2		39  // used by esc
	#define ACU_CODE_SB2		40  // used by esc
	#define ACU_CODE_DEP_TSN2	41  // used by esc
	#define ACU_CODE_HSTRAC3	42  // used by esc

	#define ACU_CODE_AB_LOT_MD	46
    #define ACU_CODE_ESC_LOT_MD	47


  #define ACU_MAX_CODE ACU_CODE_DIV_PUR2                           // FT27

  unsigned short  tranwu:15;    // transaction number
  unsigned short  merge1:1;     // transaction in merge stage
  unsigned LONGLONG txnidd;		// transaction id
  unsigned int bizdatelu;		// business date
};

struct EODTRN_SB2
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_SB2     body;
    union EODTRN_END        end;        // since struct BETDATA is of
                                        // variable size, EODTRN_END may be
                                        // put at variable position    
};

struct EODTRN_LOT2
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_LOT2    body;
    union EODTRN_END        end;        // since struct BETDATA is of
                                        // variable size, EODTRN_END may be
                                        // put at variable position   
};

struct EODTRN_HSTRAC2       // RAC2 tran in history file
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_HSTRAC2 body;
    union EODTRN_END        end;        // since struct BETDATA is of
                                        // variable size, EODTRN_END may be
                                        // put at variable position        
};

struct EODTRN_SB
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_SB      body;
    union EODTRN_END        end;        // since struct BETDATA is of
                                        // variable size, EODTRN_END may be
                                        // put at variable position        
};

struct EODTRN_LOT
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_LOT     body;
    union EODTRN_END        end;        // since struct BETDATA is of
                                        // variable size, EODTRN_END may be
                                        // put at variable position        
};

struct ACU_TRAN_LOT
{
  struct BETABLOT  bet;
};

struct EODTRN_DRCR          // debit credit adjustmen
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_DRCR    body;
    unsigned short          sizewu;
};

struct ACU_TRAN_DRCR        // debit credit adjustmen
{
  unsigned LONGLONG  amountdu;  // amount
  unsigned int       typelu;    // type // KL02 refer to drcrtxndef.h
//HL21...
    #define ACU_DEBIT_CDC	    1   // CASH DEPOSIT CLAIM
    #define ACU_DEBIT_SACCDCS	2   // SUSPENSE A/C TO CASH DEPOSIT 
				                    //	CLAIM SETTLEMENT
    #define ACU_DEBIT_EFTDC	    3   // EFT DEPOSIT CLAIM
    #define ACU_DEBIT_SACEFTDCS	4   // SUSPENSE A/C TO EFT DEPOSIT CLAIM 
				                    //	SETTLEMENT
    #define ACU_DEBIT_DBS	    5   // DEPOSIT BAD SALES
    #define ACU_DEBIT_DSHCQ     6   // DISHONOURED CHEQUE
    #define ACU_DEBIT_RBGIM     7   // REJECTED BG REIMBURSEMENT
    #define ACU_DEBIT_DFCCA	    8   // DEBIT FROM CHEQUE CONTROL ACCOUNT
    #define ACU_DEBIT_DCACWO	9   // DORMANT CONTROL A/C W/OUT
    #define ACU_DEBIT_EWUPS     10  // EFT WITHDRAWAL NOT POSTED
    #define ACU_DEBIT_EWTMO     11  // EFT BANK TIME OUT WITHDRAWAL
    #define ACU_DEBIT_CITWNP	12  // CIT WITHDRAWAL NOT POSTED
    #define ACU_DEBIT_CITBTOW	13  // CIT BANK TIME OUT WITHDRAWAL
    #define ACU_DEBIT_ESCEWNP	14  // ESC EFT WITHDRAWAL NOT POSTED
    #define ACU_DEBIT_ESCEBTO	15  // ESC EFT BANK TIME OUT
    #define ACU_DEBIT_UBSDIV	16  // UBS DIVIDEND
    #define ACU_DEBIT_BOFLTF	17  // BALANCE OVERFLOW TRANSFER
    #define ACU_DEBIT_EACEODR	18  // EMERGENCY A/C EOD REVERSING ENTRY 
				                    //	(RACEDAY ONLY)
    #define ACU_DEBIT_CITAF     19  // CIT ANNUAL FEE
    #define ACU_DEBIT_CITDF	    20  // CIT DEPOSIT FORFEITED
    #define ACU_DEBIT_CITPDAD	21  // CIT / PDA DEPOSIT
    #define ACU_DEBIT_CITRMC	22  // CIT R & M CHARGES
    #define ACU_DEBIT_BCFPDA	23  // BATTERY CHARGES FOR PDA
    #define ACU_DEBIT_DFAFFT	24  // DEBIT GFBC ACCCOUNT FOR FUND TRANSFER
    #define ACU_DEBIT_ESCDF     25  // ESC DEPOSIT FEE
    #define ACU_DEBIT_ESCFDF	26  // ESC FORFEITED DEPOSIT FEE
    #define ACU_DEBIT_BDWRI     27  // BAD DEBT WRITE IN
    #define ACU_DEBIT_SACWO     28  // SUSPENSE A/C WRITE OUT
    #define ACU_DEBIT_OUTDC	    29  // OUTSTANDING DR/CR FOR DORMANT A/C REJ W/D
    #define ACU_DEBIT_DIPFRS	30  // DIVIDEND PROFIT - RS
    #define ACU_DEBIT_DIPFFS	31  // DIVIDEND PROFIT - FS
    #define ACU_DEBIT_DIPFLS	32  // DIVIDEND PROFIT - LS
    #define ACU_DEBIT_REVENT	33  // REVERSING ENTRY
    #define ACU_DEBIT_OTHERS	34  // DEBIT ADJUSTMENT - OTHERS

    #define ACU_CREDIT_CDCTSAC	35  // CREDIT CASH DEPOSIT CLAIM TO 
				                    //	SUSPENSE A/C
    #define ACU_CREDIT_CDCS	    36  // CASH DEPOSIT CLAIM SETTLEMENT
    #define ACU_CREDIT_EFTDCTSA	37  // CREDIT EFT DEPOSIT CLAIM TO SUSPENSE A/C
    #define ACU_CREDIT_EFTDCS	38  // EFT DEPOSIT CLAIM SETTLEMENT
    #define ACU_CREDIT_CQDHOC	39  // CHEQUE DEPOSIT - H.Q. / ON-COURSE
    #define ACU_CREDIT_CDHOC	40  // CASH DEPOSIT - HQ / ON-COURSE
    #define ACU_CREDIT_CCQWD	41  // CANCELLED CHEQUE W/D
    #define ACU_CREDIT_CCQDTAC	42  // CREDIT CHEQUE DEPOSIT TO RELEVANT A/C
    #define ACU_CREDIT_EWUPS    43  // EFT WITHDRAWAL NOT POSTED
    #define ACU_CREDIT_EFTBTOS	44  // EFT BANK TIME OUT SETTLEMENT
    #define ACU_CREDIT_CITDNP	45  // CIT DEPOSIT NOT POSTED
    #define ACU_CREDIT_CITBTOS	46  // CIT BANK TIME OUT SETTLEMENT
    #define ACU_CREDIT_ESCEDNP  47  // ESC EFT DEPOSIT NOT POSTED
    #define ACU_CREDIT_ESCWP	48  // ESC EFT WITHDRAWAL POSTED
    #define ACU_CREDIT_UBSRF	49  // UBS REFUND
    #define ACU_CREDIT_BOFLTF	50  // BALANCE OVERFLOW TRANSFER
    #define ACU_CREDIT_EACSODR	51  // EMERGENCY A/C SOD REVERSING ENTRY 
				                    //	(RACEDAY ONLY)
    #define ACU_CREDIT_CITAFR	52  // CIT ANNUAL FEE REFUND
    #define ACU_CREDIT_RCITD	53  // REINSTATE CIT DEPOSIT
    #define ACU_CREDIT_CITPDADR	54  // CIT / PDA DEPOSIT REFUND
    #define ACU_CREDIT_CITRMCR	55  // CIT R & M CHARGES REFUND
    #define ACU_CREDIT_CITDRP	56  // CIT DEPOSIT REFUND - PROGRESSIVE
    #define ACU_CREDIT_TAFCITD	57  // TRANSFER ADJUSTMENT FOR CIT DEPOSIT
    #define ACU_CREDIT_TADJ	58      // TRANSFER ADJUSTMENT
    #define ACU_CREDIT_ESCDR    59  // ESC DEPOSIT FEE REFUND
    #define ACU_CREDIT_FTTGFBC	60  // FUND TRANSFER TO GFBC ACCOUNT
    #define ACU_CREDIT_BDWRO    61  // BAD DEBT WRITE OUT
    #define ACU_CREDIT_SACWIDC  62  // SUSPENSE A/C WRITE IN - DEPOSIT CLAIM
    #define ACU_CREDIT_SACWICD  63  // SUSPENSE A/C WRITE IN - CIT DEPOSIT
    #define ACU_CREDIT_RWDDAC   64  // REJ. W/D DORMANT A/C
    #define ACU_CREDIT_REJWTW   65  // REJECTED WITHDRAWAL
    #define ACU_CREDIT_RWFCAC	66  // REJECTED WITHDRAWAL FROM CLOSED ACCOUNT
    #define ACU_CREDIT_ABFN	    67  // ABFN
    #define ACU_CREDIT_OCUBRS	68  // OVER COLLATION/UNACTIONED BAD SALES - RS
    #define ACU_CREDIT_OCUBFS	69  // OVER COLLATION/UNACTIONED BAD SALES - FS
    #define ACU_CREDIT_OCUBLS	70  // OVER COLLATION/UNACTIONED BAD SALES - LS
    #define ACU_CREDIT_EXGPRS	71  // EXGRATIA PAYMENT - RS
    #define ACU_CREDIT_EXGPFS	72  // EXGRATIA PAYMENT - FS
    #define ACU_CREDIT_EXGPLS	73  // EXGRATIA PAYMENT - LS
    #define ACU_CREDIT_MBGRIN	74  // MANUAL BG REIMBURSEMENT
    #define ACU_CREDIT_REVENT	75  // REVERSING ENTRY
    #define ACU_CREDIT_OTHERS	76  // CREDIT ADJUSTMENT - OTHERS
    #define ACU_DRCR_MAT_MAX    76  // Max number that Mathndr allows
//...HL21
//HL12...
    #define ACU_CREDIT_XGR      901 // exgratia payment
    #define ACU_CREDIT_AFR      903 // CIT annual fee refund
    #define ACU_DEBIT_NAF       904 // annual fee for new cit type
    #define ACU_CREDIT_AFW      905 // cit annual fee waived
    #define ACU_CREDIT_PDR      906 // progressive deposit refund
// ...HL12

// The following are system generated credit debit adjustment
    #define ACU_CREDIT_FESCB    1000// Balance Transferred From ESC
    #define ACU_DEBIT_TVOIB     1001// Balance Transferred To Voice
    #define ACU_CREDIT_BGRIM    1002// Bank Gaurantee Reimbursement 
    #define ACU_DEBIT_SYSFOFDF  1003// Forfeited Deposit Fee By System //HL16
    #define ACU_DRCR_AUTO_MAX   1003// max. auto drcr tran code !FT13
//...HL09
  char           remarks[50+1];     // remark variable length
};

struct EODTRN_DFT           // dividend forfeited
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_DFT     body;
    unsigned short          sizewu;
};

struct ACU_TRAN_DFT         // dividend forfeited
{
  unsigned LONGLONG  amountdu;  // forfeited amount
};

struct EODTRN_DIV_PUR2      // purged transaction after Q206
{
    struct ACU_TRAN_HDR      h;
    struct ACU_TRAN_DIV_PUR2 body;    
    unsigned short           sizewu;
};

struct ACU_TRAN_DIV_PUR2    // dividend for purged transaction
{
  unsigned LONGLONG     divdu;     // dividend
  unsigned short        tranwu;    // transaction number of purged transaction
  unsigned char         typebu;    // transaction type
    #define ACU_PUR_SB  0               // SB tran
    #define ACU_PUR_LOT 1               // lottery tran
  union ACU_TRAN_PURDET det;       // SB tran details  
};

struct ACU_TRAN_LOT
{
  struct BETABLOT  bet;
};


union ACU_TRAN_PURDET       // purged transaction details
{
    struct ACU_TRAN_SB  sb;         // SB tran details
    struct ACU_TRAN_LOT lot;        // LOT tran details
};

struct ACU_TRAN_SB
{
  union  TSN      tsn;
  unsigned char   srcbu:7;    // source of sell (Changed 201108PSR)
  unsigned char   csctrn:1;  // Transaction with CSC Card (Added 201108PSR)
  struct BETDATA  bet;
};


struct EODTRN_DIV_PUR       // dividend for purged transaction
{
    struct ACU_TRAN_HDR     h;
    struct ACU_TRAN_DIV_PUR body;    
    unsigned short          sizewu;
};

struct ACU_TRAN_DIV_PUR     // dividend for purged transaction
{
  LONGLONG              divd;      // dividend
  unsigned short        tranwu;    // transaction number of purged transaction
  struct ACU_TRAN_SB    det;       // SB tran details   !FT10
};


struct LOGAB_DEPATM         // batch deposit
{
  union  LOGDEP         data;
  struct ACU_TRAN_ACA   tran;
};

union LOGDEP                                // DEPHNDR Logger record
{
    struct LOGDEPTRAN           tran;       // DEPHNDR reject or posting request
    struct LOGDEPCOMP           comp;       // DEPHNDR complete summary
};

struct LOGDEPCOMP                           // Complete Summary
{
    BOOL                        startt;     // Flag to indicate posting of this
                                            // file will begin (conversion has
                                            // finished)
    unsigned int                filidxlu;   // File index in DEPCTL (start fr 0)
    union LOGDEPCOMPD           sum;        // summary log details      PN01
};

union LOGDEPCOMPD
{
    struct LOGDEPCOMPCNV        start;  // conversion complete and start posting
    struct AA_OLTP_BATDEPSUM    end;    // end of posting result
};

struct AA_OLTP_BATDEPSUM
{
    struct BCS_DATE     valdate;        // Value date
    struct BCS_DATE     caldate;        // Calender date
    unsigned char       typebu;         // Batch deposit sender type
        #define BD_DEP_HKSC         0       // Hksc
        #define BD_DEP_EPS          1       // Eps
    unsigned int        batnumlu;       // Batch number
    unsigned short      acpttxncntwu;   // Accepted transaction count
    unsigned LONGLONG   acptamtdu;      // Accepted transaction Amount (in cents)
    unsigned LONGLONG   rechargedu;     // Recharges (in cents)
    unsigned short      rejcntwu;       // Reject transaction count
    unsigned LONGLONG   rejamtdu;       // Reject transaction Amount (in cents)

};

struct BCS_DATE
{
    char    day;
    char    month;
    short   year;
};


struct LOGDEPCOMPCNV
{
    int32_t              valdat;     // value date
    int32_t              caldat;     // calender date
    unsigned char       typebu;     // batch deposit work file type
    unsigned int        batnumlu;   // batch number
    unsigned int        firreclu;   // first record number converted
    unsigned int        lastreclu;  // last record number converted
};

struct LOGDEPTRAN                           // Reject or posting request
{
    struct AA_REJBATDEPSUB      data;       // Mail data
    unsigned int                feelu;      // recharge fee (in cents)
    unsigned int                seqlu;      // internal seq. #
    unsigned char               chanbu;     // channel #
    char                        bankcode[3];// Bank code (can be space)  // RL02
};

struct AA_REJBATDEPSUB
{
    struct BCS_DATE     valdate;        // Value date
    struct BCS_DATE     caldate;        // Calender date
    unsigned char       typebu;         // Batch deposit sender type
    unsigned int        batnumlu;       // Batch account number
    unsigned short      bankcodewu;     // internal bank/terminal #	EH37
    char                bankacc[BCS_ACCNUM_LEN];    // Bank account number
    unsigned int        seqnumlu;       // Input sequence number
    unsigned int        clubaccnumlu;   // Club account number
    char                reqclubaccnumacc[AA_REQACCNUM_LEN];    // Request club account number
    unsigned LONGLONG   amtdu;          // Amount (in cents)
};

struct  LOGRDC          // log message
{
    LONGLONG  		activityIdd;	// sp3 - for passing back to wchndr
    unsigned int    msnlu;      // msn
    unsigned short  callerbu;   // WC/RWCC
    unsigned short  funcodewu;  // rdc function code
    union LOGRDCID  i;
    union LOGRDCD   d;
};

union   LOGRDCD         // log data
    {
        struct LOGRDCMSCH       msch;       // meeting schedule
        struct LOGRDCSPSTT      spstt;      // change sell/ pay status
        struct LOGRDCSUB        sub;        // subsitute
        struct LOGRDCSCR        scr;        // scratching
        struct LOGRDCRES        res;        // result
        struct LOGRDCPTT        ptt;        // change post time
        struct LOGRDCDSA        dsa;        // disable all-up betting by race   // JC10
        struct LOGRDCEAB        eab;        // enable ext branch lossing consolation // JC07
        struct LOGRDCRAD        rad;        // pool rad/claim details input
        struct LOGRDCRCW        rcw;        // race close interval
        struct LOGRDCBSE        bse;        // bad sale expire
        struct LOGRDCRWI        rwi;        // race close warning interval
        struct LOGRDCAFE        afe;        // allup enabling
        struct LOGRDCAFM        afm;        // allup formula enabling
        struct LOGRDCAWL        awl;        // all up re-investment warning limit
        struct LOGRDCMBV        mbv;        // max. bet value
        struct LOGRDCPAYL       payl;       // payout limit
        struct LOGRDCTBD        tbd;        // tb deposit parameters
        struct LOGRDCTBW        tbw;        // tb (EFT) withdrawal parameters
        struct LOGRDCEDB        edb;        // enable/disable deposit betting
        struct LOGRDCEFT        eft;        // eft cv min
        struct LOGRDCNBD        nbd;        // next business date
        struct LOGRDCPMC        pmc;        // peak hour minimum cost
        struct LOGRDCLBV        lbv;        // large bet warning value
        struct LOGRDCLDV        ldv;        // large div warning value
        struct LOGRDCRCLW       rclw;       // race close warning
        struct LOGRDCRRPT       rrpt;       // racing report request
        struct LOGRDCPUMIN      pumin;      // partial unit minimum cost    // JC01
        struct LOGRDCLCLW       lclw;       // lottery close warning
        struct LOGRDCLSCH       lsch;       // lottery schedule
        struct LOGRDCLDD        ldd;        // change draw date
        struct LOGRDCLOD        lod;        // change openning date
        struct LOGRDCLCD        lcd;        // change closing date
//        struct LOGRDCLCT        lct;        // change closing time // CS11
        struct LOGRDCLRES       lres;       // lottery result
        struct LOGRDCLPRZ       lprz;       // lottery prizes
        struct LOGRDCPRZSTS     lpsts;      // change prizes status
        struct LOGRDCLWPS       lwps;       // winner pass request from RWCC
        struct LOGRDCAEN        aen;        // ccgame enabling
//        struct LOGRDCABE        abe;        // ccgame unit investment
        struct LOGRDCAPR        apr;        // ccgame prizes amount
        struct LOGRDCLBS        lbs;        // lottery bad sale expire
        struct LOGRDCLCI        lci;        // lottery close warning interval
        struct LOGRDCLMS        lms;        // lottery selection range
        struct LOGRDCLBA        lba;        // lottery unit investment
        struct LOGRDCLRPT       lrpt;       // lottery report request
        struct LOGRDCCVEC       cvec;       // CV encashment checking       // JC05
        struct LOGRDCLSCMTG     lscmtg;     // losing inv con ctl - meeting     // JC07
        struct LOGRDCLSCRCE     lscrce;     // losing inv con ctl - race        // JC07
        struct LOGRDCLSCPOL     lscpol;     // losing inv con ctl - pool        // JC07
        struct LOGRDCLMER       lmer;       // snowball merge       // CS11
  };

  struct  LOGRDCSPSTT             // change sell/ pay status
    {
        unsigned int    vbt1:1;         // off-course indicator // CS03..
        unsigned int    did1:1;         // on-course indicator
        unsigned int    esc1:1;         // off-course indicator //..CS03
        unsigned int    onc1:1;         // on-course indicator
        unsigned int    ofc1:1;         // off-course indicator
        unsigned int    :11;            // unused               // CS03
    };


  struct  LOGRDCMSCH      // meeting schedule 
    {
        unsigned short     setwu;       // file set no. allocated
        unsigned short     mnumwu;      // meeting no.
        int32_t             mdat;        // meeting date (bitty date)
        unsigned short     trcwu;       // total no. of race
        unsigned short     nrciwu;      // on-cousre race close interval (min.)
        unsigned short     frciwu;      // off-course race close interval(min.)
        unsigned short     bsiwu;       // bad sale expire interval (sec.)
        unsigned short     mrpwu;       // meeting retention period (in day)
        unsigned int       cstartlu;    // collation start
        LONGLONG           rstartd;     // next aup rin file VBN
        struct LOGRDCRSCH  rsch[RDS_MAXRACE+1]; // race schedule portion, [0] not used
    };


union   LOGRDCID
    {
        struct LOGRDCIDR  r;
        struct LOGRDCIDL  l;
//        struct LOGRDCIDCC c;
    };

struct LOGSBC          // log message
{
    struct LOGSBCH      h;              // header
    union LOGSBCD       d;              // data
};


//    *******************************************************************
//    *                                                                 *
//    *   � COPYRIGHT.  The Hong Kong Jockey Club                       *
//    *                                                                 *
//    *   This software, which contains confidential material, is       *
//    *   private and confidential and is the property and copyright    *
//    *   of The Hong Kong Jockey Club (the Club). No part of this      *
//    *   document may be reproduced, stored in a retrieval system      *
//    *   or transmitted in any form or by any means, electronic,       *
//    *   mechanical, chemical, photocopy, recording or otherwise       *
//    *   without the prior written permission of the Club              *
//    *                                                                 *
//    *******************************************************************
//
//    Author : Edward Hon                01-NOV-2000
//
//    Mod :     JC01        12-NOV-2002
//              add partial unit bet minimum cost
//
//              JC02        20-FEB-2003
//              both "Change lottery closing date" and
//              "Change lottery closing time" contains new closing date/time
//
//              CS03        30-OCT-2003
//              add more area for selling to support OLTP-AB
//
//              JC04        18-OCT-2004
//              remove wcm expand bit as no one use it.  Forget why keep the original
//              wcm in the logger, may be just want to display the wcm from WC when
//              do the logdmp and audit
//
//              JC05        20-DEC-2004
//              add CV encashment checking parameters (178)
//
//              JC06        22-JUL-2005
//              limit the max. # of lottery prize in logger record
//
//              JC07        30-AUG-2005
//              1. combine logger for lottery, GBL/MK6 and normal/ccgame
//              2. add logger record for losing investment consolation (353/354/355)
//              3. change logger for struct LOGRDCLBV
//              4. add msnl, caller in logger for use of RWCC handshake
//              5. use logger structure of code 330 for code 356 also 
//
//              JN08        20-OCT-2005
//              For pools stop sell in a race, change 1 = WPQQP instead of -1
//
//              JC09        10-NOV-2005
//              use int32_t for change post date time
//
//              JC10        16-NOV-2005
//              use bitmap for disable aup betting
//
//              CS11        06-DEC-2005
//              1. modify lottery input to support advance draw selling
//                 - add snowball flag, draw's short/long name in LOGRDCLSCH 
//                 - add slave draw index in LOGRDCIDL
//                 - add new logger record for draw merge (357) LOTRECLMER
//              2. delete structure LOGRDCLCT as replace by LOGRDCLCD and
//                 add new variable of lottery closing date
//
#ifndef LOGRDCDEF_H

#define LOGRDCDEF_H 1

#include <time.h>
#include <limits.h> //JC07
#include "udtypedef.h"
#include "rdsdef.h"
#include "lotdef.h"
//#include "wcmsgdef.h"
#include "bstypedef.h"

#define LOGRDC_MAXDHEAT         3                               // maximum dead heat
#define LOGRDC_RESSIZ           LOGRDC_MAXDHEAT * RDS_MAXRES    // race result size
#define LOGRDC_FLDRES           32                              // field result indicator in result

//#define LOGRDC_LRGBET_NOPOOL    5                               // define same as RDCPAR.H
#define LOGRDC_LRGDIV_NOPOOL    3                               // define same as RDCPAR.H

#define LOGRDC_MAX_ENT          UCHAR_MAX                       // maximum entry count

#pragma pack(1)

// MEETING OPTION

struct  LOGRDCRSCH      // race schedule portion
    {
        unsigned short  pstwu;          // race post time
        unsigned short  fszwu;          // field size
        unsigned short  distwu;         // race distance
        unsigned int    nraclu;         // on-course pools bitmap
        unsigned int    fraclu;         // off-course pools bitmap
        unsigned int    pleglu[RDS_MAXPOOL];    // pool legs bitmap
    };

struct  LOGRDCMSCH      // meeting schedule 
    {
        unsigned short     setwu;       // file set no. allocated
        unsigned short     mnumwu;      // meeting no.
        int32_t             mdat;        // meeting date (bitty date)
        unsigned short     trcwu;       // total no. of race
        unsigned short     nrciwu;      // on-cousre race close interval (min.)
        unsigned short     frciwu;      // off-course race close interval(min.)
        unsigned short     bsiwu;       // bad sale expire interval (sec.)
        unsigned short     mrpwu;       // meeting retention period (in day)
        unsigned int       cstartlu;    // collation start
        LONGLONG           rstartd;     // next aup rin file VBN
        struct LOGRDCRSCH  rsch[RDS_MAXRACE+1]; // race schedule portion, [0] not used
    };

// abandon meeting, no more data log

struct  LOGRDCRCW       // race close interval
    {
        unsigned short  occtwu;         // on-course close interval (min)
        unsigned short  ofctwu;         // off-course close interval (min)
    };

struct  LOGRDCSPSTT             // change sell/ pay status
    {
        unsigned int    vbt1:1;         // off-course indicator // CS03..
        unsigned int    did1:1;         // on-course indicator
        unsigned int    esc1:1;         // off-course indicator //..CS03
        unsigned int    onc1:1;         // on-course indicator
        unsigned int    ofc1:1;         // off-course indicator
        unsigned int    :11;            // unused               // CS03
    };

struct  LOGRDCBSE       // meeting bad sale interval change 
    {
        unsigned short  bswu;           // new bad sale interval (in secs)
    }; 

// RACE OPTION

struct  LOGRDCSUB       // race substitute runner input
    {
        unsigned char   subbu[RDS_MAXSUB];      // substitute
    };

struct  LOGRDCSCR       // race scratching input
    {
        unsigned long long    scrlu;          // scratching bit map
        unsigned long long		nopbu;          // no. of placing for place
    };

struct  LOGRDCRES       // race result input
    {
        unsigned long long    reslu[RDS_MAXRES];  // race result bit map
        unsigned int		full1:1;            // full result
        unsigned int		:15;                // unused
    };

struct  LOGRDCPTT       // race post time
    {
        int32_t          pttDate;            // new post date time   // JC09
//        unsigned short  timewu;         // new race post time
    };

// Re-activate all-up post race pass, no more data log

// The following messages:
// start sell a pool, stop pay a pool, pool refund, cancel pool refund  
// will use the same struct LOGRDCSPSTT

// race close message, no more data log
// race collation final, no more data log
// race stop pay all pools, no more data log

// POOL OPTION
struct WCM          // information for each winning combination
{
        LONGLONG        divd;                   // dividend (in cents)
        unsigned LONGLONG    wclu[RDS_MAXWCSIZ];     // win comb bitmap
        unsigned LONGLONG    orgwclu[RDS_MAXWCSIZ];  // original win comb bitmap
};

struct  LOGRDCRAD       // pool rad/claim details input
    {
        unsigned char   subbu[RDS_MAXLEG][RDS_MAXSUB];  // sub. runner #
        unsigned long long    scrlu[RDS_MAXLEG];              // scratching bitmap 
        unsigned short  nowu;                           // no. of result and dividend
        unsigned char   sflgbu;                         // substitute existing flag
        unsigned short    ovfl1:1;                        // dividend overflow
        unsigned short    clm1:1;                         // claim
        unsigned short    punit1:1;                       // partial unit
        unsigned short    unoff1:1;                       // unofficial
//        unsigned int    expand1:1;                      // wcm expanded       // JC04
        unsigned short    :12;                            // unused
        struct WCM      wcm[RDS_MAXDIV];                // wcm info for each wcm
    };

struct  LOGRDCPEW       // pool exotic winner
    {
        unsigned short  reswu[LOGRDC_RESSIZ+1][RDS_MAXLEG+1];
                                // each leg race result 
    };
// CS11..
struct LOGNAME
{
    char                shorts[LOT_SNAME_LEN]; // snowball draw short name // CS03
    char                longs[LOT_NAME_LEN];   // snowball draw long name // CS03
};
// ..CS11

//LOTTERY OPTION

struct  LOGRDCLSCH      // lottery schedule
    {

        int32_t          ddate;          // draw date
        int32_t          odate;          // opening date
        int32_t          cdate;          // closing date & time
// ctimewu no use any more, but want to keep the structure size,
// just set it as filler        // JC
//        unsigned short  ctimewu;        // closing time in hhmm
//        unsigned short  fillerwu;       // closing time in hhmm
        struct LOGNAME  name;           // lottery name             // CS11
        unsigned short  retwu;          // retention period
        unsigned char   drawIdxbu;      // draw index used
        unsigned char   fileIdxbu;      // file index used
        unsigned short  lastLotSeqwu;   // last lottery sequence
        BOOL            xdrawt;         // snowball draw (true=1)   // CS11
        unsigned char   drefIdxbu;      // reference file entry     // CS11
    };

// lottery start sell, no more data log
// lottery stop sell, no more data log
// lottery close, no more data log
// lottery collation final, no more data log

struct  LOGRDCLDD       // change of lottery draw date
    {
        int32_t          nddate;         // new draw date
    };

struct  LOGRDCLOD       // change of lottery opening date
    {
        int32_t          nodate;         // new lottery opening date
    };

struct  LOGRDCLCD       // change of lottery closing date               // JC02..
    {
        int32_t          ncdate;         // new closing date(same date > 24:00) //  CS11
        int32_t          ncdattim;       // new closing date time(next date&time > 24:00) // CS11
        char            reopenb;        // 1= function for re-open draw
    };

//struct  LOGRDCLCT       // change of lottery closing time               // CS11..           
//    {
//        int32_t          ncdate;         // new lottery closing date time
//        unsigned short  ctimewu;        // new lottery closing time in hhmm
//        char            reopenb;        // 1= function for re-open draw // ..CS11
//    };                                                                  // ..JC02

struct  LOGRDCLRES      // lottery result
    {
        unsigned short  noswu[LOT_MAXDNO];      // drawn no.+extra no.
    };

struct  LOGRDCLPRZ      // lottery prize
    {
        unsigned char       gtypbu;             // cc game type
        LONGLONG            przd[LOT_MAXPRZ_CUR];   // prize value  -1=overflow // JC06
        struct LOTPZSTS     sts[LOT_MAXPRZ_CUR];    // prize status             // JC06
    };  

struct LOGRDCPRZSTS     // stop pay/claim/cancel claim lottery prize
    {
        unsigned char   gtypbu;         // cc game type
        short           pznow;          // prize id(s) bitmap 
    };

struct LOGRDCLWPS       // winner pass request from RWCC
    {
        unsigned short  numwu[LOT_MAXDNO];        // result; numwu[0]=unused
    };

// PARAMETER OPTION


struct  LOGRDCRWI       // race close warning interval
    {
        unsigned short  intwu;      // new interval (in min.)
    };

struct  LOGRDCMBV       // max. bet value
    {
        unsigned LONGLONG  mbvdu;   // max. bet value (in cents)
        unsigned LONGLONG  micvdu;  // max. manuaL issue cv (in cents)
        unsigned LONGLONG  esccvdu; // max. esc cv (in cents)
        unsigned LONGLONG  svtcvdu; // max. auto svt cv (in cents)
        unsigned LONGLONG  optcvdu; // max. auto opt cv (in cents)
    };

struct  LOGRDCAFE       // allup enabling
    {
        unsigned int    enable1:1;      // enable indicator
        unsigned int    :15;            // unused
    };

struct  LOGRDCAFM       // allup formula enabling
    {
        BOOL   enabu[RDS_MAXAPOOL][RDS_MAXAFML];   // enable flag
    };

struct  LOGRDCAWL       // all up re-investment warning limit
    {
        unsigned LONGLONG   aupdu;      // warning limit (in cents)
    };

struct  LOGRDCPAYL      // pay limit
    {
        unsigned LONGLONG   hodu;       // pay at ho limit (in cents) 
        unsigned LONGLONG   ocdu;       // pay at original ctr limit(cents)
    };

struct LOGRDCLBS        // lottery bad sale expired
    {
        unsigned short  bsiwu;          // bad sale expired (in sec)
    };

struct LOGRDCLCI        // lottery close warning internal
    {
        unsigned short  cwiwu;          // close warning int.(in min)
    };

struct LOGRDCLMS
    {
        unsigned short  selbaswu;       // base selection number
        unsigned short  selmaxwu;       // maximum selection number
        unsigned short  gblbaswu;       // base goldball number
        unsigned short  gblmaxwu;       // maximum goldball number
    };

struct LOGRDCLBA
    {
        unsigned int    amtlu;          // lottery base investment
    };

struct  LOGRDCLRPT       // lottery report request
    {
        unsigned char   idbu;           // report id, refer rpbdef.h
    };

struct  LOGRDCTBD       // tb deposit parameters
    {
        unsigned LONGLONG   amtdu;      // min. deposit amt (in cents)
        unsigned short      stimwu;     // start time in 4 sec.
        unsigned short      etimwu;     // end time in 4 sec.
    };

struct  LOGRDCTBW       // tb (EFT) withdrawal parameters
    {
        unsigned LONGLONG   mindu;      // min. withd. amt (in cents)
        unsigned LONGLONG   maxdu;      // max. per day (in cents)
        unsigned short      cntwu;      // max. withd. count per day
        unsigned short      dohwu;      // dep on hold time in min. 
    };

struct LOGRDCDSA        // disable all-up betting by race   // JC10
    {
        unsigned int    dsalu;          // disable aup betting bitmap
                                        // ( bit 1 => race 1 ...)
    };

struct LOGRDCEAB        // enable/disable all up betting
    {
        unsigned int    ena1:1;         // enable indicator
        unsigned int    :15;            // unused
    };

struct LOGRDCEDB        // enable/disable deposit betting
    {
        unsigned int    ena1:1;         // enable indicator
        unsigned int    :15;            // unused
    };

struct  LOGRDCNBD       // next business date
    {
         int32_t         dat;            // date
    };

struct  LOGRDCPMC       // peak hour minimum cost
    {
        unsigned int    cblu;           // cb in $
    };

struct  LOGRDCEFT       // eft cv min
    {
        unsigned int    rdlu;           // raceday in $
        unsigned int    nrdlu;          // non-raceday in $
    };

struct  LOGRDCLBV_ENT                   // JC07..
    {
        unsigned char       betTypebu;
        unsigned LONGLONG   amtdu;
    };

struct  LOGRDCLBV       // large bet W/P/Q/QPL/TCE
    {
        unsigned char           numbu;
        struct  LOGRDCLBV_ENT   ent[LOGRDC_MAX_ENT];
    };                                  // ..JC07

struct  LOGRDCLDV       // large div [] refer BETTYPDEF.H, e.g. BETYPE_STD for std
    {
        unsigned LONGLONG ldvdu[LOGRDC_LRGDIV_NOPOOL];// large div.in $
    };

struct  LOGRDCAEN       // Concurrent Game Enable/Disable Flag
    {
        BOOL              enat;         // enable(1), disable(0) flag
    };

//struct  LOGRDCABE       // Concurrent Game Unit Bet Value
//    {
//        unsigned short    ubvwu;        // unit bet value (in $)
//    };
  
struct  LOGRDCAPR       // Concurrent Game Default Prize
    {
        unsigned LONGLONG dpvdu;        // default prize value 
                                        // in cents per $ of investment
    };

struct  LOGRDCCCDED     // Concurrent Game Deductions
    {
        unsigned short    taxwu;        // % tax deduction (in % *100)
        unsigned short    comwu;        // % commission deduction (in %*100)
        unsigned short    fundwu;       // % fund deduction (in %*100)
    };

struct  LOGRDCRCLW       // race close warning
    {
        unsigned short  hourwu;         // hour
        unsigned short  minwu;          // minute
        unsigned int    onc1:1;         // on-course indicator
        unsigned int    ofc1:1;         // off-course indicator
        unsigned int    :14;            // unused
    };

struct  LOGRDCRRPT       // racing report request
    {
        unsigned char   idbu;           // report id, refer rpbdef.h
    };

// since the unit bet and min. total cost kept in rdscom is by bet type,
// the pool id in header of this message is kept for the bet type instead
// i.e. 0=W-P, 1=WIN, 2=PLA...
struct  LOGRDCPUMIN      // partial unit bet minimum cost   // JC01..
    {
        unsigned int    unitlu;         // partial unit bet in $
        unsigned int    costlu;         // minimum total cost amount in $
    };                                                      // ..JC01

struct  LOGRDCLCLW       // lottery close warning
    {
        unsigned short  hourwu;         // hour
        unsigned short  minwu;          // minute
    };

struct LOGRDCCVEC       // CV encashment checking       // JC05
{
    BOOL                        enat;       // checking enable flag
    unsigned LONGLONG           amtdu;      // remaining amount
    unsigned short              percwu;     // % used for betting
};

struct LOGRDCLSCMTG_ENT                                                 // JC07..
{
    unsigned char           tierbu;                 // tier id
    unsigned char           chanbu;                 // channel id, AB or CB
    BOOL                    enat;                   // enable flag
    unsigned LONGLONG       amtdu;                  // amount in cents
};

// for struct LOGRDCLSCMTG, if corresponding meeting index >= RDS_MAXMEET,
// the message is for the global change on external branch enabing,
// there should be no more data for tier/channel, i.e. numbu == 0
// WCHNDR will update the global external branch enabling to each defined meeting.
struct LOGRDCLSCMTG                                 // losing inv con ctl - meeting
{
    BOOL                    enat;                   // enable flag for external branches
    unsigned char           numbu;                  // # of tier
    struct LOGRDCLSCMTG_ENT ent[LOGRDC_MAX_ENT];    // by tier by channel data
};

struct LOGRDCLSCRCE_ENT
{
    unsigned char           racebu;                 // race #
    BOOL                    enat;                   // enable flag
};

struct LOGRDCLSCRCE                                 // losing inv con ctl - race
{
    unsigned char           chanbu;                 // channel id, AB or CB
    unsigned char           numbu;                  // # of entry
    struct LOGRDCLSCRCE_ENT ent[LOGRDC_MAX_ENT];    // by race by channel  
};

struct LOGRDCLSCPOL_ENT
{
    unsigned char           tierbu;                 // tier id
    unsigned char           poolbu;                 // pool id
    unsigned short          percwu;                 // % * 100
};

struct LOGRDCLSCPOL                                 // losing inv con ctl - pool
{
    unsigned char           chanbu;                 // channel id, AB or CB
    unsigned char           numbu;                  // # of entry
    struct LOGRDCLSCPOL_ENT ent[LOGRDC_MAX_ENT];    // by tier by pool data
};

struct LOGRDCLMER                                   // draw merge    // CS11..
{
    unsigned char              masteridxbu;        // draw index of master draw 
    unsigned char              slaveidxbu;         // draw index of slave draw 
};                                                                   // ..CS11

union   LOGRDCD         // log data
    {
        struct LOGRDCMSCH       msch;       // meeting schedule
        struct LOGRDCSPSTT      spstt;      // change sell/ pay status
        struct LOGRDCSUB        sub;        // subsitute
        struct LOGRDCSCR        scr;        // scratching
        struct LOGRDCRES        res;        // result
        struct LOGRDCPTT        ptt;        // change post time
        struct LOGRDCDSA        dsa;        // disable all-up betting by race   // JC10
        struct LOGRDCEAB        eab;        // enable ext branch lossing consolation // JC07
        struct LOGRDCRAD        rad;        // pool rad/claim details input
        struct LOGRDCRCW        rcw;        // race close interval
        struct LOGRDCBSE        bse;        // bad sale expire
        struct LOGRDCRWI        rwi;        // race close warning interval
        struct LOGRDCAFE        afe;        // allup enabling
        struct LOGRDCAFM        afm;        // allup formula enabling
        struct LOGRDCAWL        awl;        // all up re-investment warning limit
        struct LOGRDCMBV        mbv;        // max. bet value
        struct LOGRDCPAYL       payl;       // payout limit
        struct LOGRDCTBD        tbd;        // tb deposit parameters
        struct LOGRDCTBW        tbw;        // tb (EFT) withdrawal parameters
        struct LOGRDCEDB        edb;        // enable/disable deposit betting
        struct LOGRDCEFT        eft;        // eft cv min
        struct LOGRDCNBD        nbd;        // next business date
        struct LOGRDCPMC        pmc;        // peak hour minimum cost
        struct LOGRDCLBV        lbv;        // large bet warning value
        struct LOGRDCLDV        ldv;        // large div warning value
        struct LOGRDCRCLW       rclw;       // race close warning
        struct LOGRDCRRPT       rrpt;       // racing report request
        struct LOGRDCPUMIN      pumin;      // partial unit minimum cost    // JC01
        struct LOGRDCLCLW       lclw;       // lottery close warning
        struct LOGRDCLSCH       lsch;       // lottery schedule
        struct LOGRDCLDD        ldd;        // change draw date
        struct LOGRDCLOD        lod;        // change openning date
        struct LOGRDCLCD        lcd;        // change closing date
//        struct LOGRDCLCT        lct;        // change closing time // CS11
        struct LOGRDCLRES       lres;       // lottery result
        struct LOGRDCLPRZ       lprz;       // lottery prizes
        struct LOGRDCPRZSTS     lpsts;      // change prizes status
        struct LOGRDCLWPS       lwps;       // winner pass request from RWCC
        struct LOGRDCAEN        aen;        // ccgame enabling
//        struct LOGRDCABE        abe;        // ccgame unit investment
        struct LOGRDCAPR        apr;        // ccgame prizes amount
        struct LOGRDCLBS        lbs;        // lottery bad sale expire
        struct LOGRDCLCI        lci;        // lottery close warning interval
        struct LOGRDCLMS        lms;        // lottery selection range
        struct LOGRDCLBA        lba;        // lottery unit investment
        struct LOGRDCLRPT       lrpt;       // lottery report request
        struct LOGRDCCVEC       cvec;       // CV encashment checking       // JC05
        struct LOGRDCLSCMTG     lscmtg;     // losing inv con ctl - meeting     // JC07
        struct LOGRDCLSCRCE     lscrce;     // losing inv con ctl - race        // JC07
        struct LOGRDCLSCPOL     lscpol;     // losing inv con ctl - pool        // JC07
        struct LOGRDCLMER       lmer;       // snowball merge       // CS11
  };

  struct  LOTPZSTS        // lottery prize status
{
    unsigned int        div1:1;                 // div in
    unsigned int        ovfl1:1;                // overflow
    unsigned int        clm1:1;                 // claim
    unsigned int        dfix1:1;                // div fixed
    unsigned int        na1:1;                  // prize not applicable 
    unsigned int        :11;                    // unused
};

struct  LOGRDCIDR       // racing id
    {
        unsigned short  indexwu;        // meeting index
        unsigned short  racewu;         // race #
        short           poolw;          // JN08 for message(307), stop sell pools in a race 
                                        //      pool id, all pools =0, win/pla/qin/qpl = 1  
                                        //      for other message, pool id define refer to RDSDEF.H
        int32_t          mdate;          // meeting date
        unsigned char   locbu;          // location
        unsigned char   daybu;          // day
    };

struct  LOGRDCIDL       // lottery id
    {
        unsigned short  yearwu;         // year
        unsigned short  drawwu;         // draw
        unsigned short  typewu;         // lottery type         // lottery type, e.g. MK6/ GBL
        unsigned char   typbu;          // cc game type         // ccgame, e.g. NOR, AON
        unsigned char   subtbu;         // cc game sub type     // subgame, e.g. OUG10
        unsigned char   idxbu;          // lottery index
        unsigned char   sidxbu;         // slave draw index=draw index+1, 0=unused // CS11 
        unsigned short  sdrawwu;        // slave draw no. // CS11
    };

//struct  LOGRDCIDCC      // concurrent game id
//    {
//        unsigned char           idbu;   // cc game id
//        unsigned char           typbu;  // cc game type     // NORMAL/CCGAMES
//        unsigned char           subtbu; // cc game sub type
//    };

union   LOGRDCID
    {
        struct LOGRDCIDR  r;
        struct LOGRDCIDL  l;
//        struct LOGRDCIDCC c;
    };

struct  LOGRDC          // log message
    {
		LONGLONG  		activityIdd;	// sp3 - for passing back to wchndr
        unsigned int    msnlu;      // msn
        unsigned short  callerbu;   // WC/RWCC
        unsigned short  funcodewu;  // rdc function code
        union LOGRDCID  i;
        union LOGRDCD   d;
    };

#pragma pack(1)

#endif
