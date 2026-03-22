
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

import io
from .translation import char_to_seis
from .constants import BITS_PER_SEIS_SYMBOL, SEIS_SYMBOLS_PER_BLOCK,BYTES_PER_BLOCK,HEADER_SIZE

class Encoder:
    def __init__(self):
        self.block = 0
        self.symbols_in_block = 0
        self.total_symbol_count = 0
        self.result = None

    def encode(self, content: str) -> bytes:
        self._reset_internal_variables()
        self._write_to_header(0) # allocate header space

        for char in content:
            self._write_result(char_to_seis(char))
            self.total_symbol_count += 1

        if self.symbols_in_block != 0:
            self._handle_leftover_space()

        self._write_to_header(self.total_symbol_count) # write how many total seisimo symbols there are

        return self.result.getvalue()
    
    def _reset_internal_variables(self):
        self.block = 0
        self.symbols_in_block = 0
        self.total_symbol_count = 0
        self.result = io.BytesIO()

    def _write_result(self, seis_dec: int):
        self.block = (self.block << BITS_PER_SEIS_SYMBOL) | seis_dec
        self.symbols_in_block += 1
        if self.symbols_in_block == SEIS_SYMBOLS_PER_BLOCK:
            self._flush_block()

    def _flush_block(self):
        self.result.write(self.block.to_bytes(BYTES_PER_BLOCK, 'big'))
        self.block = 0
        self.symbols_in_block = 0

    def _handle_leftover_space(self):
        pad = SEIS_SYMBOLS_PER_BLOCK - self.symbols_in_block
        self.block <<= (pad * BITS_PER_SEIS_SYMBOL)
        self._flush_block()

    def _write_to_header(self, header_bytes: int):
        self.result.seek(0)
        self.result.write(header_bytes.to_bytes(HEADER_SIZE, "big"))
        self.result.seek(0, io.SEEK_END)


if __name__ == "__main__":
    print()
