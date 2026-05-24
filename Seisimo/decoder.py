import io
from .translation import seis_to_char
from .constants import BITS_PER_SEIS_SYMBOL, SEIS_SYMBOLS_PER_BLOCK, BYTES_PER_BLOCK, HEADER_SIZE

class Decoder:
    def decode(self, content: io.IOBase) -> str:
        symbol_count = self._get_header_value(content)
        content.seek(HEADER_SIZE, io.SEEK_SET) # move stream to after header
        
        result = []
        
        while symbol_count > 0:
            result += self._read_block(content, min(symbol_count, SEIS_SYMBOLS_PER_BLOCK))
            symbol_count -= SEIS_SYMBOLS_PER_BLOCK

        return "".join(result)

    def _read_block(self, content: io.IOBase, count: int):
        block = int.from_bytes(content.read(BYTES_PER_BLOCK), 'big')
        string = self._translate_block(block, count)
        return string
    
    def _translate_block(self, block: int, cycles: int):
        # goes from left right to account for MSB
        string = []
        shift = (SEIS_SYMBOLS_PER_BLOCK - 1) * BITS_PER_SEIS_SYMBOL 
        for _ in range(cycles):
            string.append(seis_to_char((block>> shift) & 0b00111111))
            shift -= BITS_PER_SEIS_SYMBOL
        return string
        
    def _get_header_value(self, content: io.IOBase) -> int:
        """
        Reads the total seis symbol count from the file header.

        :param content: A readable/seekable binary stream of encoded seis data.
        :returns count: total amount of seis symbol 
        """
        curr = content.tell()
        content.seek(0, io.SEEK_SET)
        header_value = int.from_bytes(content.read(HEADER_SIZE), 'big')
        content.seek(curr, io.SEEK_SET)
        return header_value
        
        