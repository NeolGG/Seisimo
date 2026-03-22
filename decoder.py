import io
from .translation import seis_to_char
from .constants import BITS_PER_SEIS_SYMBOL, SEIS_SYMBOLS_PER_BLOCK, BYTES_PER_BLOCK

class Decoder:
    def __init__(self):
        self.block= 0
        self.total_symbol_count = 0
        self.result = None
    
    def decode(self, content: io.IOBase) -> str:
        self._reset_internal_variables()
        self.total_symbol_count = self._get_header_value(content)
        content.seek(4, io.SEEK_SET) # move stream to after header
        
        while self.total_symbol_count > 0:
            self._read_block(content, min(self.total_symbol_count, SEIS_SYMBOLS_PER_BLOCK))
            self.total_symbol_count -= SEIS_SYMBOLS_PER_BLOCK

        return "".join(self.result)

    def _read_block(self, content: io.IOBase, count: int):
        self.block = int.from_bytes(content.read(BYTES_PER_BLOCK), 'big')
        self._translate_block(count)
        self.block = 0
    
    def _translate_block(self, cycles: int):
        # goes from left right to account for MSB
        shift = (SEIS_SYMBOLS_PER_BLOCK - 1) * BITS_PER_SEIS_SYMBOL 
        for _ in range(cycles):
            self.result.append(seis_to_char((self.block >> shift) & 0b00111111))
            shift -= BITS_PER_SEIS_SYMBOL
        
    def _get_header_value(self, content: io.IOBase) -> int:
        """
        Reads the total seis symbol count from the file header.

        :param content: A readable/seekable binary stream of encoded seis data.
        :returns: The total number of seis symbols encoded in the file.
        :note: Stream-safe — restores the stream position after reading.
        """
        curr = content.tell()
        content.seek(0, io.SEEK_SET)
        header_value = int.from_bytes(content.read(4), 'big')
        content.seek(curr, io.SEEK_SET)
        return header_value

    def _reset_internal_variables(self):
        self.block = 0
        self.total_symbol_count = 0
        self.result = list()
        