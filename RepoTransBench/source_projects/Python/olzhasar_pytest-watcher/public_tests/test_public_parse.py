from pytest_watcher import parse

def test_parse_additional_args(monkeypatch):
    args = ["-v", "-k", "AnotherKeyword"]
    parsed = parse.parse_args(args)
    assert "-v" in args
    assert parsed.k == "AnotherKeyword" or getattr(parsed, "k", None) == "AnotherKeyword"