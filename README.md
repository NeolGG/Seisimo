# Seisimo

Seisimo is a personal project that implements a custom 6-bit text encoding format to better understand text encoding and bit manipulation.

## How it works

Standard ASCII uses 8 bits per character. Seisimo uses 6 bits by supporting only letters, digits, and spaces.

**Symbol table**

| Range | Seis values | Characters |
|---|---|---|
| 0 | 0 | space |
| 1 – 26 | 000001 – 011010 | a – z |
| 27 – 36 | 011011 – 100100 | 0 – 9 |
| 62 | 111110 | null (unknown char) |

**Packing**

Four 6-bit symbols are packed into one 3-byte (24-bit) block, MSB first:

```
[ sym1 | sym2 | sym3 | sym4 ]
  6 bits each = 24 bits = 3 bytes
```

**File format**

| Bytes | Content |
|---|---|
| 0 – 3 | 4-byte big-endian header: total symbol count |
| 4 – EOF | Packed 3-byte blocks |

The header stores the total seisimo symbol count for decoding.

## Usage

```python
import io
from Seisimo import Encoder, Decoder

encoder = Encoder()
decoder = Decoder()

encoded: bytes = encoder.encode("hello world 42")
decoded: str   = decoder.decode(io.BytesIO(encoded))
```

To encode/decode a file, handle I/O in the caller:

```python
with open("input.txt", "r") as f:
    encoded = encoder.encode(f.read())

with open("input.txt.seis", "wb") as f:
    f.write(encoded)

with open("input.txt.seis", "rb") as f:
    decoded = decoder.decode(f)
```

## Notes

- Lowercase letters for now with plans to implement capital letters via an ALT state.
- Unsupported characters encode to the null symbol (62) and decode to an empty string.

## Plans

1. Add ALT state
2. Add uppercase support
3. add popular punctuation