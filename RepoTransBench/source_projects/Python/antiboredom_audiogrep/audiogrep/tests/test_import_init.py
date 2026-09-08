def test_import_from_init():
    import audiogrep
    assert hasattr(audiogrep, "convert_to_wav")
    assert hasattr(audiogrep, "transcribe")