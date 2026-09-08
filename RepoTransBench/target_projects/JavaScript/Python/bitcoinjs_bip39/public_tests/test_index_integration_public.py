import pytest
import os

# Public test mnemonics/entropy/PASSWORD should be different
VALID_MNEMONIC = "legal winner thank year wave sausage worth useful legal winner thank yellow"
INVALID_MNEMONIC = "hello world example lorem ipsum dolor sit amet consectetuer adipiscing elit"
VALID_ENTROPY = "2e8905819b8723fe2c1d161860e5ee1830318dbf49a83bd451cfb8440c28bd6f"
INVALID_ENTROPY = "xyz_not_a_hex_1234"
PASSWORD = "OpenAI123!"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import index as bip39
except ImportError:
    bip39 = None

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_generates_mnemonic_from_entropy_public():
    mnemonic = bip39.entropyToMnemonic(VALID_ENTROPY)
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split(' ')) == 24

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_generates_entropy_from_mnemonic_public():
    entropy = bip39.mnemonicToEntropy(VALID_MNEMONIC)
    assert isinstance(entropy, str)
    assert entropy == VALID_ENTROPY

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_validates_correct_mnemonic_public():
    assert bip39.validateMnemonic(VALID_MNEMONIC) is True

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_invalidates_incorrect_mnemonic_public():
    assert bip39.validateMnemonic(INVALID_MNEMONIC) is False

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_entropyToMnemonic_invalid_entropy_throws_public():
    with pytest.raises(Exception):
        bip39.entropyToMnemonic(INVALID_ENTROPY)

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_mnemonicToEntropy_invalid_mnemonic_throws_public():
    with pytest.raises(Exception):
        bip39.mnemonicToEntropy(INVALID_MNEMONIC)

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_generateRandom_mnemonic_public():
    mnemonic = bip39.generateMnemonic()
    assert isinstance(mnemonic, str)
    length = len(mnemonic.split(' '))
    assert length == 12 or length == 24
    assert bip39.validateMnemonic(mnemonic) is True

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_generates_and_validates_seed_from_mnemonic_public():
    import asyncio
    loop = asyncio.get_event_loop()
    seed = loop.run_until_complete(bip39.mnemonicToSeed(VALID_MNEMONIC, PASSWORD))
    assert isinstance(seed, (bytes, bytearray))
    assert len(seed) == 64

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_generates_and_validates_seedSync_from_mnemonic_public():
    seed = bip39.mnemonicToSeedSync(VALID_MNEMONIC, PASSWORD)
    assert isinstance(seed, (bytes, bytearray))
    assert len(seed) == 64

@pytest.mark.skipif(bip39 is None, reason='bip39(index.py) implementation not found')
def test_supports_custom_wordlists_public():
    french = getattr(bip39.wordlists, 'french', None) if hasattr(bip39, 'wordlists') else None
    assert isinstance(french, list), 'french wordlist present'
    assert len(french) == 2048
    mnemonic = bip39.entropyToMnemonic(VALID_ENTROPY, french)
    assert isinstance(mnemonic, str)
    assert len(mnemonic.split(' ')) == 24