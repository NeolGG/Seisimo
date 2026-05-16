from .constants import ALPHA_DISPLACEMENT, NUM_DISPLACEMENT

def char_to_seis(char: str) -> int:
    char = char.lower()
    if char.isalpha():
        return ord(char) - ALPHA_DISPLACEMENT
    elif char.isdigit():
        return ord(char) - NUM_DISPLACEMENT
    elif char == ' ':
        return 0
    else:
        return 62

def seis_to_char(seis_decimal: int) -> str:
    if 0 < seis_decimal < 27:
        return chr(seis_decimal + ALPHA_DISPLACEMENT)
    elif 26 < seis_decimal < 37:
        return chr(seis_decimal + NUM_DISPLACEMENT)
    elif seis_decimal == 0:
        return ' '
    else:
        return ''