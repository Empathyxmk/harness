import pyzlib

def test_public_constants_present():
    meta_fields = [
        "NO_COMPRESSION", "DEFAULT_COMPRESSION", "FILTERED", "HUFFMAN_ONLY",
        "_COPYRIGHT", "_DESCRIPTION"
    ]
    for k in meta_fields:
        assert hasattr(pyzlib, k), f"public constant missing: {k}"