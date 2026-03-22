import io
from Seisimo import Decoder, Encoder

sample1 = 'the quick brown fox jumps over the lazy dog 42 times before stopping at zone 9 pack 5 wizards jot down 16 quirky facts about 83 brave explorers heading to sector 7'
sample2 = 'solar panels on building 4 generate 72 kilowatts per hour while unit 3 stores 150 units daily across 9 floors team b logged 48 errors in module 6 before patch 2 resolved all issues by friday'

encoder = Encoder()
decoder = Decoder()

def roundtrip(text: str) -> str:
    encoded = encoder.encode(text)
    return decoder.decode(io.BytesIO(encoded))

def test_roundtrip_sample1():
    assert roundtrip(sample1) == sample1

def test_roundtrip_sample2():
    assert roundtrip(sample2) == sample2

def test_single_char():
    assert roundtrip('a') == 'a'

def test_single_digit():
    assert roundtrip('7') == '7'

def test_space():
    assert roundtrip('hello world') == 'hello world'

def test_full_block():
    # exactly 4 symbols — no leftover
    assert roundtrip('abcd') == 'abcd'

def test_partial_block():
    # 1, 2, 3 symbols — exercises leftover path
    assert roundtrip('a') == 'a'
    assert roundtrip('ab') == 'ab'
    assert roundtrip('abc') == 'abc'

def test_numbers():
    assert roundtrip('abc 123') == 'abc 123'

def test_unknown_chars_ignored():
    # punctuation encodes to 62 (null), decodes to ''
    result = roundtrip('hi!')
    assert result == 'hi'

