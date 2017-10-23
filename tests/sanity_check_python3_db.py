"""
Checking to see if basic PACSY database operations work with python3.
"""
from pluq import dbtools


def reasobble_shift_pacsy():
    """
    Returns a reasonable shift from the PACSY database for the input
    res, atom and snd_str.
    """
    sql = r"""SELECT C_MODE, C_STD FROM CS_STATS_DB
    WHERE RES = 'A'
    AND ATOM_NAME = 'CA'
    AND SND_STRC in ('H', 'X')"""
    print(sql)
