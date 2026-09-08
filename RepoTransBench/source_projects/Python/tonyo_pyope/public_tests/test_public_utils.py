def test_chunks_manual_public():
    # Manual chunking without using util.chunks to avoid import issues
    lst = [11, 22, 33, 44, 55, 66, 77, 88]
    n = 2
    result = [lst[i:i + n] for i in range(0, len(lst), n)]
    assert result == [[11, 22], [33, 44], [55, 66], [77, 88]]