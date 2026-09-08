def test_different_read_all_returns_stream():
    from io import BytesIO
    test_string = "PublicTestContent123"
    input_stream = BytesIO(test_string.encode("utf-8"))
    # Read all bytes
    bytes_data = input_stream.read()
    assert test_string == bytes_data.decode("utf-8")