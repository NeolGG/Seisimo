
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
    def encode(self, content: str) -> bytes:
        result = io.BytesIO()
        self._set_header_value(result, 0) # allocate header space
        result.seek(HEADER_SIZE, io.SEEK_SET) # move stream to after header
        characters = list(content)
        symbol_count = len(characters)

        while len(characters) >= 4:
            a = char_to_seis(characters.pop(0))
            b = char_to_seis(characters.pop(0))
            c = char_to_seis(characters.pop(0))
            d = char_to_seis(characters.pop(0))
            self._write_block(result, [a, b, c, d])

        self._handle_leftover_space(result, [char_to_seis(c) for c in characters])
        self._set_header_value(result, symbol_count)

        return result.getvalue()
        
    def _write_block(self, result: io.BytesIO, seis_block: list):
        block_to_write = 0
        for b in seis_block:
            block_to_write = (block_to_write << BITS_PER_SEIS_SYMBOL) | b
        result.write(block_to_write.to_bytes(BYTES_PER_BLOCK, 'big'))

    def _handle_leftover_space(self, result: io.BytesIO, block: list[int]):
        if len(block) == 0: return
        block_to_write = 0
        pad = SEIS_SYMBOLS_PER_BLOCK - len(block)
        for b in block:
            block_to_write = (block_to_write << BITS_PER_SEIS_SYMBOL) | b
        block_to_write <<= (pad * BITS_PER_SEIS_SYMBOL)
        result.write(block_to_write.to_bytes(BYTES_PER_BLOCK, 'big'))

    def _set_header_value(self, result: io.BytesIO,  header_bytes: int):
        result.seek(0)
        result.write(header_bytes.to_bytes(HEADER_SIZE, "big"))
        result.seek(0, io.SEEK_SET)

if __name__ == "__main__":
    print()
