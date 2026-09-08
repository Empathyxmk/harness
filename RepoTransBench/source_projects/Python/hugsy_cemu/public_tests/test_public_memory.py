def test_public_placeholder_memory():
    # Placeholder - ensure some coverage while using different data.
    a = bytearray(b"memory_public")
    a[5] = ord('P')
    assert a[5] == ord("P")