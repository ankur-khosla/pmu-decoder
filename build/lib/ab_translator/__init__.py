"""
AB Race Translator Package

A Python package for translating AB Racing messages from C++ LOGAB structures.
Converted from C++ ABRace.cpp and related files.
"""

from .ab_race import ABRace
from .ab_msg_translator import ABMsgTranslator
from .data_structures import Msg, LogabHdr, LogabRac, LogabData
from .constants import *

def create_ab_race():
    """
    Factory function to create an ABRace translator instance.
    
    Returns:
        ABRace: Configured race translator instance
    """
    return ABRace()

__version__ = "1.0.0"
__author__ = "Converted from C++ ABRace"

__all__ = [
    'ABRace',
    'ABMsgTranslator', 
    'Msg',
    'LogabHdr',
    'LogabRac',
    'LogabData',
    'create_ab_race',
    # Constants
    'BETTYP_WINPLA', 'BETTYP_WIN', 'BETTYP_PLA', 'BETTYP_QIN', 'BETTYP_QPL',
    'BETTYP_DBL', 'BETTYP_TCE', 'BETTYP_FCT', 'BETTYP_QTT', 'BETTYP_DQN',
    'BETTYP_TBL', 'BETTYP_TTR', 'BETTYP_6UP', 'BETTYP_DTR', 'BETTYP_TRIO',
    'BETTYP_QINQPL', 'BETTYP_CV', 'BETTYP_MK6', 'BETTYP_PWB', 'BETTYP_AUP',
    'BETTYP_FF', 'BETTYP_BWA', 'BETTYP_CWA', 'BETTYP_CWB', 'BETTYP_CWC',
    'BETTYP_IWN',
    'LOGAB_CODE_RAC',
    'STORE_TYPE_STRING', 'STORE_TYPE_INTEGER', 'STORE_TYPE_CHAR'
]
