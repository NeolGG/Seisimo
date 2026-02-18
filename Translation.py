from Constants import *

def ascii_to_seis(ascii_decimal: int) -> int:
    if 96 < ascii_decimal < 123:
        return ascii_decimal - ALPHA_DISPLACEMENT
    elif 47 < ascii_decimal < 58:
        return ascii_decimal - NUM_DISPLACEMENT
    elif ascii_decimal == 32:
        return 0
    else:
        return 62

def seis_to_ascii(seis_decimal: int) -> int:
    if 0 < seis_decimal < 27:  
        return seis_decimal + ALPHA_DISPLACEMENT
    elif 26 < seis_decimal < 37:  
        return seis_decimal + NUM_DISPLACEMENT
    elif seis_decimal == 0:
        return 32
    else:
        return 0 