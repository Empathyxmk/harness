import pytest
from src import farmhash

def test_hash32_returns_number_for_string_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    assert isinstance(farmhash.hash32(input_string), int)

def test_hash32_returns_number_for_buffer_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    input_buffer = input_string.encode('utf-8')
    assert isinstance(farmhash.hash32(input_buffer), int)

@pytest.mark.parametrize("bad_input", [123, {}, None])
def test_hash32_throws_for_invalid_input(bad_input):
    with pytest.raises(TypeError):
        farmhash.hash32(bad_input)

def test_hash32withseed_returns_number_for_string_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    seed = 123
    assert isinstance(farmhash.hash32WithSeed(input_string, seed), int)

def test_hash32withseed_returns_number_for_buffer_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    input_buffer = input_string.encode('utf-8')
    seed = 123
    assert isinstance(farmhash.hash32WithSeed(input_buffer, seed), int)

@pytest.mark.parametrize("bad_seed", ['a', 1.23, None])
def test_hash32withseed_throws_for_invalid_seed(bad_seed):
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    if bad_seed is None:
        with pytest.raises(TypeError):
            farmhash.hash32WithSeed(input_string)
    else:
        with pytest.raises(TypeError):
            farmhash.hash32WithSeed(input_string, bad_seed)

def test_hash32withseed_throws_for_invalid_input():
    seed = 123
    with pytest.raises(TypeError):
        farmhash.hash32WithSeed(123, seed)

def test_hash64_returns_bigint_for_string_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    assert isinstance(farmhash.hash64(input_string), int)

def test_hash64_returns_bigint_for_buffer_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    input_buffer = input_string.encode('utf-8')
    assert isinstance(farmhash.hash64(input_buffer), int)

@pytest.mark.parametrize("bad_input", [123, {}, None])
def test_hash64_throws_for_invalid_input(bad_input):
    with pytest.raises(TypeError):
        farmhash.hash64(bad_input)

def test_hash64withseed_returns_bigint_for_string_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    seed = 123
    assert isinstance(farmhash.hash64WithSeed(input_string, seed), int)

def test_hash64withseed_returns_bigint_for_buffer_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    input_buffer = input_string.encode('utf-8')
    seed = 123
    assert isinstance(farmhash.hash64WithSeed(input_buffer, seed), int)

@pytest.mark.parametrize("bad_seed", ['a', 4.67, None])
def test_hash64withseed_throws_for_invalid_seed(bad_seed):
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    if bad_seed is None:
        with pytest.raises(TypeError):
            farmhash.hash64WithSeed(input_string)
    else:
        with pytest.raises(TypeError):
            farmhash.hash64WithSeed(input_string, bad_seed)

def test_hash64withseed_throws_for_invalid_input():
    seed = 123
    with pytest.raises(TypeError):
        farmhash.hash64WithSeed(123, seed)

def test_hash64withseeds_returns_bigint_for_string_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    seed = 123
    seed2 = 456
    assert isinstance(farmhash.hash64WithSeeds(input_string, seed, seed2), int)

def test_hash64withseeds_returns_bigint_for_buffer_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    input_buffer = input_string.encode('utf-8')
    seed = 123
    seed2 = 456
    assert isinstance(farmhash.hash64WithSeeds(input_buffer, seed, seed2), int)

@pytest.mark.parametrize("args", [
    ('b', 456),
    (123, None),
    (23.4, 456),
    (123,),
    ()
])
def test_hash64withseeds_throws_for_invalid_seeds(args):
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    with pytest.raises(TypeError):
        farmhash.hash64WithSeeds(input_string, *args)

def test_hash64withseeds_throws_for_invalid_input():
    seed = 123
    seed2 = 456
    with pytest.raises(TypeError):
        farmhash.hash64WithSeeds(123, seed, seed2)

def test_fingerprint32_returns_number_for_string_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    assert isinstance(farmhash.fingerprint32(input_string), int)

def test_fingerprint32_returns_number_for_buffer_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    input_buffer = input_string.encode('utf-8')
    assert isinstance(farmhash.fingerprint32(input_buffer), int)

@pytest.mark.parametrize("bad_input", [555, {}, None])
def test_fingerprint32_throws_for_invalid_input(bad_input):
    with pytest.raises(TypeError):
        farmhash.fingerprint32(bad_input)

def test_fingerprint64_returns_bigint_for_string_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    assert isinstance(farmhash.fingerprint64(input_string), int)

def test_fingerprint64_returns_bigint_for_buffer_input():
    input_string = 'The quick brown fox jumped over the lazy sleeping dog'
    input_buffer = input_string.encode('utf-8')
    assert isinstance(farmhash.fingerprint64(input_buffer), int)

@pytest.mark.parametrize("bad_input", [555, {}, None])
def test_fingerprint64_throws_for_invalid_input(bad_input):
    with pytest.raises(TypeError):
        farmhash.fingerprint64(bad_input)

def test_fingerprint64signed_returns_signed_bigint_for_string():
    unsigned = farmhash.fingerprint64('1footrue')
    signed = farmhash.fingerprint64signed('1footrue')
    assert isinstance(signed, int)
    # Simulate signed 64-bit
    unsigned_s = str(unsigned)
    if unsigned > 2**63 - 1:
        expected_signed = str(unsigned - 2**64)
    else:
        expected_signed = unsigned_s
    assert str(signed) == unsigned_s or str(signed) == expected_signed

def test_fingerprint64signed_returns_signed_bigint_for_buffer():
    buffer = b'1footrue'
    unsigned = farmhash.fingerprint64(buffer)
    signed = farmhash.fingerprint64signed(buffer)
    assert isinstance(signed, int)
    unsigned_s = str(unsigned)
    if unsigned > 2**63 - 1:
        expected_signed = str(unsigned - 2**64)
    else:
        expected_signed = unsigned_s
    assert str(signed) == unsigned_s or str(signed) == expected_signed