import pytest
from src import farmhash

def test_hash32_returns_number_for_string_input_public():
    input_string = 'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.hash32(input_string), int)

def test_hash32_returns_number_for_buffer_input_public():
    input_buffer = b'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.hash32(input_buffer), int)

@pytest.mark.parametrize("bad_input", [False, [], None])
def test_hash32_throws_for_invalid_input_public(bad_input):
    with pytest.raises(TypeError):
        farmhash.hash32(bad_input)

def test_hash32withseed_returns_number_for_string_input_public():
    input_string = 'Pack my box with five dozen liquor jugs!'
    seed = 321
    assert isinstance(farmhash.hash32WithSeed(input_string, seed), int)

def test_hash32withseed_returns_number_for_buffer_input_public():
    input_buffer = b'Pack my box with five dozen liquor jugs!'
    seed = 321
    assert isinstance(farmhash.hash32WithSeed(input_buffer, seed), int)

@pytest.mark.parametrize("bad_seed", ['seed', -2.5, None])
def test_hash32withseed_throws_for_invalid_seed_public(bad_seed):
    input_string = 'Pack my box with five dozen liquor jugs!'
    if bad_seed is None:
        with pytest.raises(TypeError):
            farmhash.hash32WithSeed(input_string)
    else:
        with pytest.raises(TypeError):
            farmhash.hash32WithSeed(input_string, bad_seed)

def test_hash32withseed_throws_for_invalid_input_public():
    seed = 321
    with pytest.raises(TypeError):
        farmhash.hash32WithSeed(None, seed)

def test_hash64_returns_bigint_for_string_input_public():
    input_string = 'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.hash64(input_string), int)

def test_hash64_returns_bigint_for_buffer_input_public():
    input_buffer = b'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.hash64(input_buffer), int)

@pytest.mark.parametrize("bad_input", [False, [], None])
def test_hash64_throws_for_invalid_input_public(bad_input):
    with pytest.raises(TypeError):
        farmhash.hash64(bad_input)

def test_hash64withseed_returns_bigint_for_string_input_public():
    input_string = 'Pack my box with five dozen liquor jugs!'
    seed = 321
    assert isinstance(farmhash.hash64WithSeed(input_string, seed), int)

def test_hash64withseed_returns_bigint_for_buffer_input_public():
    input_buffer = b'Pack my box with five dozen liquor jugs!'
    seed = 321
    assert isinstance(farmhash.hash64WithSeed(input_buffer, seed), int)

@pytest.mark.parametrize("bad_seed", [{}, 8.9, None])
def test_hash64withseed_throws_for_invalid_seed_public(bad_seed):
    input_string = 'Pack my box with five dozen liquor jugs!'
    if bad_seed is None:
        with pytest.raises(TypeError):
            farmhash.hash64WithSeed(input_string)
    else:
        with pytest.raises(TypeError):
            farmhash.hash64WithSeed(input_string, bad_seed)

def test_hash64withseed_throws_for_invalid_input_public():
    seed = 321
    with pytest.raises(TypeError):
        farmhash.hash64WithSeed([], seed)

def test_hash64withseeds_returns_bigint_for_string_input_public():
    input_string = 'Pack my box with five dozen liquor jugs!'
    seed = 321
    seed2 = 654
    assert isinstance(farmhash.hash64WithSeeds(input_string, seed, seed2), int)

def test_hash64withseeds_returns_bigint_for_buffer_input_public():
    input_buffer = b'Pack my box with five dozen liquor jugs!'
    seed = 321
    seed2 = 654
    assert isinstance(farmhash.hash64WithSeeds(input_buffer, seed, seed2), int)

@pytest.mark.parametrize("args", [
    ('foo', 654), 
    (321, []), 
    ({}, 654), 
    (321,), 
    ()
])
def test_hash64withseeds_throws_for_invalid_seeds_public(args):
    input_string = 'Pack my box with five dozen liquor jugs!'
    with pytest.raises(TypeError):
        farmhash.hash64WithSeeds(input_string, *args)

def test_hash64withseeds_throws_for_invalid_input_public():
    seed = 321
    seed2 = 654
    with pytest.raises(TypeError):
        farmhash.hash64WithSeeds(None, seed, seed2)

def test_fingerprint32_returns_number_for_string_input_public():
    input_string = 'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.fingerprint32(input_string), int)

def test_fingerprint32_returns_number_for_buffer_input_public():
    input_buffer = b'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.fingerprint32(input_buffer), int)

@pytest.mark.parametrize("bad_input", [True, [], None])
def test_fingerprint32_throws_for_invalid_input_public(bad_input):
    with pytest.raises(TypeError):
        farmhash.fingerprint32(bad_input)

def test_fingerprint64_returns_bigint_for_string_input_public():
    input_string = 'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.fingerprint64(input_string), int)

def test_fingerprint64_returns_bigint_for_buffer_input_public():
    input_buffer = b'Pack my box with five dozen liquor jugs!'
    assert isinstance(farmhash.fingerprint64(input_buffer), int)

@pytest.mark.parametrize("bad_input", [True, [], None])
def test_fingerprint64_throws_for_invalid_input_public(bad_input):
    with pytest.raises(TypeError):
        farmhash.fingerprint64(bad_input)

def test_fingerprint64signed_returns_signed_bigint_for_string_public():
    unsigned = farmhash.fingerprint64('xyzzytest')
    signed = farmhash.fingerprint64signed('xyzzytest')
    assert isinstance(signed, int)
    unsigned_s = str(unsigned)
    if unsigned > 2**63 - 1:
        expected_signed = str(unsigned - 2**64)
    else:
        expected_signed = unsigned_s
    assert str(signed) == unsigned_s or str(signed) == expected_signed

def test_fingerprint64signed_returns_signed_bigint_for_buffer_public():
    buffer = b'xyzzytest'
    unsigned = farmhash.fingerprint64(buffer)
    signed = farmhash.fingerprint64signed(buffer)
    assert isinstance(signed, int)
    unsigned_s = str(unsigned)
    if unsigned > 2**63 - 1:
        expected_signed = str(unsigned - 2**64)
    else:
        expected_signed = unsigned_s
    assert str(signed) == unsigned_s or str(signed) == expected_signed