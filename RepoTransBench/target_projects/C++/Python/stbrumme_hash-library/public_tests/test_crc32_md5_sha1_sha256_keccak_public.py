import pytest
import hashlib
try:
    import zlib
except ImportError:
    zlib = None

# For Keccak-256 and SHA3-256, we try to use pycryptodome, fallback to pysha3 if available.
# (Standard Python >=3.6 has hashlib.sha3_256, but NO keccak256).
def keccak256_pycryptodome(data: bytes) -> str:
    try:
        from Crypto.Hash import keccak
        k = keccak.new(digest_bits=256)
        k.update(data)
        return k.hexdigest()
    except ImportError:
        # Try fallback - this will only work if pysha3 is installed and it exposes keccak_256
        try:
            import sha3
            return sha3.keccak_256(data).hexdigest()
        except ImportError:
            raise RuntimeError('Keccak-256 support requires pycryptodome or pysha3!')

def sha3_256_hash(data: bytes) -> str:
    try:
        return hashlib.sha3_256(data).hexdigest()
    except AttributeError:
        try:
            import sha3
            return sha3.sha3_256(data).hexdigest()
        except ImportError:
            raise RuntimeError('SHA3-256 not supported (install pysha3 or use Python 3.6+)')

def crc32b(data: bytes) -> str:
    # zlib.crc32 returns number
    return f"{zlib.crc32(data)&0xffffffff:08x}"

@pytest.mark.parametrize("input_data, exp_crc32, exp_md5, exp_sha1, exp_sha256, exp_sha3, exp_keccak", [
    (
        "hello",
        "3610a686",
        "5d41402abc4b2a76b9719d911017c592",
        "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        "644bcc7e56437304039e05c05bcb6a663b1e9cf1f14e2aa0d2fae921d6c5c6d1",
        "06e6a7cea485ac1734ba73e2586445e0be4aa7236a1bc86b871d94e0ebd6c166"
    ),
    (
        "publictest",
        "c8ae25a3",
        "eef060cceac087a4b71a5847dd1b48f1",
        "6d92cd561f80e1ac140b567ff327b09965f1cb9a",
        "7c38b523cf63f2c9a1ee8687c0c908d8f8eeca7c209a3a16548ff09b8bf10297",
        "a1c9963d7fa1f6bb7ec35b7d2fcbdf02c1f59e763fd85853bd431b3861beb50a",
        "3d2b2f73b7ca203232d2efc5733fe117a8eef36a8be1e66e3675a2b907e1b85d"
    ),
    (
        "hash123!",
        "e44be85d",
        "64e7f2986525bb3467cd7265a05c4e13",
        "790dbde0e9b4955d7a0a776e199824c03777d0cf",
        "e0b5cdd740cf8a66fd7e49faaf9da6afdd1ae8cfa2d33ae1b179c5faf5a0989c",
        "6a444a0fd6e985d8b9c3ab7c30f8915db736617db1d081f8d21db03049d96c20",
        "09124ecf440a11a18e853a7bebbfae6ea37aa9dcdb7ceec36da1aba920167e24"
    ),
    (
        "A longer, multi-line\ntest string with 123 and !@# symbols.",
        "69ed0394",
        "4bda373d4e57e216266cba221c11e2fb",
        "5c3eff903f7e9bb5c515b3a58a443e2ccf8c1d86",
        "286b506e7263e1485d4b44d5e966b89ba1bc33458d6eab1c5d1c8e909fae948e",
        "9aada4e41f2f1efe9342bf2d38ffc3f5617e15641bdded0ccb4d858816e01a0e",
        "aee18a30d268f50e6b22c02849a49c13be604e9c1ef92e11a6bef4ab02c05f75"
    )
])
def test_all_hashes(input_data, exp_crc32, exp_md5, exp_sha1, exp_sha256, exp_sha3, exp_keccak):
    b = input_data.encode("utf-8")
    # CRC32
    if zlib is not None:
        assert crc32b(b) == exp_crc32
    # MD5
    assert hashlib.md5(b).hexdigest() == exp_md5
    # SHA1
    assert hashlib.sha1(b).hexdigest() == exp_sha1
    # SHA256
    assert hashlib.sha256(b).hexdigest() == exp_sha256
    # SHA3-256
    assert sha3_256_hash(b) == exp_sha3
    # Keccak-256
    assert keccak256_pycryptodome(b) == exp_keccak