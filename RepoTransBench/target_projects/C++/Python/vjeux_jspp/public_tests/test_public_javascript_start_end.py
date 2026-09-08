def test_public_js_start_end_macro_like(capsys):
    arr = [10, 20, 30]
    print("arrlen=" + str(len(arr)))
    captured = capsys.readouterr()
    assert "arrlen=3" in captured.out