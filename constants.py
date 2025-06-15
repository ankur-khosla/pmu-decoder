# Constants
ACP01 = 20
ACP02 = 21

# Message Type Definition, Only ABRace / ABCan related is migrated
LOGAB_CODE_RAC = 6
LOGAB_CODE_CAN = 8

LOGAB_SRC_VOICE      = 1    # voice
LOGAB_SRC_CIT        = 2    # cit, use LOGAB_SOURCE_DID
LOGAB_SRC_MAT        = 3    # mat
LOGAB_SRC_CB_BT      = 4    # cb bt
LOGAB_SRC_EWIN       = 5    # ewin, use LOGAB_SOURCE_DID
LOGAB_SRC_OLD        = 6    # old protocol by channel and system
LOGAB_SRC_BAT_DEP    = 7    # batch deposit - tb #
LOGAB_SRC_EFT_CB     = 8    # eft from cb, use LOGAB_SOURCE_CBBT
LOGAB_SRC_EFT_CIT    = 9    # eft from cit, use LOGAB_SOURCE_DID
LOGAB_SRC_SBC        = 10   # soccer betting control
LOGAB_SRC_AUTO       = 11   # system generated
LOGAB_SRC_EOD        = 12   # eod generated
LOGAB_SRC_WC         = 13   # wagering control
LOGAB_SRC_POL        = 14   # pre-online
LOGAB_SRC_OPR        = 15   # operator
LOGAB_SRC_EFT_EWIN   = 16   # eft from ewin, use LOGAB_SOURCE_DID
LOGAB_SRC_TBASD      = 17   # TBASD Added Q407
LOGAB_SRC_EFT_TBASD  = 18   # TBASD Added Q407
LOGAB_SRC_CB_EWAL    = 19   # eWallet added for SP21a
LOGAB_SRC_EFT_FPS    = 20   # FPS added for SP21a
LOGAB_SRC_MAX        = 29   # max type

DEV_TYP_MPB      = 1   # MPB (Mobile phone/cit2)
DEV_TYP_CIT3     = 2   # CIT3
DEV_TYP_CIT3A    = 3   # CIT3a
DEV_TYP_CIT5     = 4   # CIT5
DEV_TYP_CIT6     = 5   # CIT6
DEV_TYP_TWM      = 6   # TWM
DEV_TYP_CITPDA   = 7   # CIT PDA
DEV_TYP_ESC      = 8   # ESC
DEV_TYP_INET     = 9   # INTERNET
DEV_TYP_CIT8     = 10  # CIT8
DEV_TYP_JCBW     = 11  # JCBW, Jockey club betting WEB
DEV_TYP_AMBS     = 12  # AMBS, Advance mobile betting service
DEV_TYP_WLPDA    = 13  # WLPDA, Wireless PDA
DEV_TYP_IPPHONE  = 14  # IP-PHONE Q107
DEV_TYP_JCBWEKBA = 17  # JCBW (eKBA)
DEV_TYP_MBSN     = 19  # MBSN → APINOW
DEV_TYP_IOSBS    = 20  # iPhone (MSR201103)
DEV_TYP_JCMOW    = 21  # MOBILE WEB (MSR201103)
DEV_TYP_IBT      = 22  # IBT (2011IBT)
DEV_TYP_AOSBS    = 23  # AOSBS (2011NOV)
DEV_TYP_APISMC   = 24  # APISMC (2011NOV)
DEV_TYP_APITD    = 25  # APITD (2011NOV)
DEV_TYP_IBUT     = 26  # IBUT (2013MAR)
DEV_TYP_API3HK   = 27  # API3HK (2013AUG) → APIWC
DEV_TYP_IBUA     = 28  # IBUA (2014NOV)
DEV_TYP_WOSBS    = 29  # Window Phone (MSR2015)
DEV_TYP_MASBAI   = 30  # MASBAI (APR2021)
DEV_TYP_MASBAA   = 31  # MASBAA (APR2021)


MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

BETTYP_WINPLA        = 0
BETTYP_WIN           = 1
BETTYP_PLA           = 2
BETTYP_QIN           = 3
BETTYP_QPL           = 4
BETTYP_DBL           = 5
BETTYP_TCE           = 6
BETTYP_QTT           = 7
BETTYP_DQN           = 8
BETTYP_TBL           = 9
BETTYP_TTR           = 10
BETTYP_6UP           = 11
BETTYP_DTR           = 12
BETTYP_TRIO          = 13
BETTYP_QINQPL        = 14
BETTYP_CV            = 15
BETTYP_MK6           = 16
BETTYP_PWB           = 17
BETTYP_AUP           = 18
BETTYP_SB            = 19  # pari-mutuel collated soccer bet
BETTYP_SB_FO         = 20  # fixed-odds collated soccer bet
BETTYP_SB_EXO        = 21  # exotic soccer bet
BETTYP_SB_AUP_PM     = 22  # all-up soccer bet parimutuel
BETTYP_SB_AUP_FO_CTL = 23  # controlled fixed odds all-up
BETTYP_SB_AUP_FO_NON = 24  # non-controlled fixed odds all-up
BETTYP_SB_SCT_FO     = 25  # section bet (PN03)
BETTYP_SB_MIX_FO     = 26  # mixed bet type - fixed odds (PN02, PN03)
BETTYP_FF            = 27  # first four (Q406)
BETTYP_BWA           = 28  # bracket win (Q406)
BETTYP_CWA           = 29  # composite win
BETTYP_CWB           = 30  # composite win
BETTYP_CWC           = 31  # composite win
BETTYP_IWN           = 33  # insurance win
BETTYP_FCT           = 34  # FCT AUG2020 L311
BETTYP_MAX           = 50  # maximum number of bet types

# Sub code for add-on game
BETTYP_AON      = 1
BETTYP_OEG      = 2
BETTYP_MHG      = 3
BETTYP_ENR      = 4
BETTYP_OUG      = 5
BETTYP_AON_MAX  = 5  # max. number of add-on games

# Bet type category
BETYPE_STD  = 0
BETYPE_EXO  = 1
BETYPE_AUP  = 2
BETYPE_LOT  = 3  # VC01
BETYPE_NA   = -1

# TODO: Confime with Paul: Overlappings
# Combined all-up and non all-up bet type codes (work file definitions)
BETTYP_AWP   = 18
BETTYP_AWN   = 19
BETTYP_APL   = 20
BETTYP_AQN   = 21
BETTYP_AQP   = 22
BETTYP_ATR   = 23
BETTYP_AQQP  = 24
BETTYP_ATC   = 25
BETTYP_AQT   = 26



RDS_MAXFLD   =  62  # max. field size. support 34 starters