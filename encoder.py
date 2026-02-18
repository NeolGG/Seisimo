
'''
000000 000000 000000 000000
00000000 00000000 00000000
'''

'''
a = 97
a->1->000001

'''

'''

'''

from typing import BinaryIO
from Translation import ascii_to_seis, seis_to_ascii
from Constants import BUFFER, BITS_PER_SEIS_SYMBOL, SEIS_SYMBOLS_PER_BLOCK

class Encoder:
    def __init__(self):
        self.bit_buffer = 0
        self.seis_symbol_count = 0
        self.total_seis_symbol_count = 0
        self.input_file = None
        self.output_file = None
    
    def encode(self, filename: str):
        self.input_file = open(filename, "r")
        self.output_file = open(f"{filename}.seis", "wb")
        
        # allocate header space
        self._write_to_header() 
    
        while 1:
            chunk = self.input_file.read(BUFFER)
            if not chunk: break
            for char in chunk:
                self._write_to_file(ascii_to_seis(ord(char.lower())))
                self.total_seis_symbol_count += 1
                
        if self.seis_symbol_count != 0:
            self._handle_leftover_space()

        # write header value
        self._write_to_header(self.total_seis_symbol_count) 
        
        self.input_file.close()
        self.output_file.close()
    
    def _write_to_file(self, seis_dec: int):
        self.bit_buffer = (self.bit_buffer << BITS_PER_SEIS_SYMBOL) | seis_dec
        self.seis_symbol_count+=1
        if self.seis_symbol_count == SEIS_SYMBOLS_PER_BLOCK:
            self._flush_bit_buffer() 
            return
        
    def _flush_bit_buffer(self):
        self.output_file.write(self.bit_buffer.to_bytes(3,'big'))
        self.bit_buffer = 0
        self.seis_symbol_count = 0     
    
    def _handle_leftover_space(self):
        pad = SEIS_SYMBOLS_PER_BLOCK - self.seis_symbol_count
        self.bit_buffer <<= (pad * BITS_PER_SEIS_SYMBOL)
        self._flush_bit_buffer() 
    
    def _write_to_header(self, header_bytes: bytes = 0):
        self.output_file.seek(0)
        self.output_file.write((header_bytes).to_bytes(4, "big"))
