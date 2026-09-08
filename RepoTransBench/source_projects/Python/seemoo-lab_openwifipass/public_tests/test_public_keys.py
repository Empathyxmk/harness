from openwifipass import Keys


def test_deterministic_key_generation_public():
    # Use different seed for public test
    seed = b"anotherdeterministicseed"
    priv, pub = Keys.generateKeyPairFromSeed(seed)
    priv2, pub2 = Keys.generateKeyPairFromSeed(seed)
    assert priv == priv2 and pub == pub2


def test_ephemeral_key_generation_public():
    priv, pub = Keys.generateEphemeralKeyPair()
    assert isinstance(priv, bytes)
    assert isinstance(pub, bytes)
    assert len(priv) == 32
    assert len(pub) == 32

def test_key_exchange_public():
    # Use different seeds for public key exchange
    a_priv, a_pub = Keys.generateKeyPairFromSeed(b"seedA_public")
    b_priv, b_pub = Keys.generateKeyPairFromSeed(b"seedB_public")
    s1 = Keys.computeSharedSecret(a_priv, b_pub)
    s2 = Keys.computeSharedSecret(b_priv, a_pub)
    assert s1 == s2
    assert isinstance(s1, bytes) and len(s1) == 32