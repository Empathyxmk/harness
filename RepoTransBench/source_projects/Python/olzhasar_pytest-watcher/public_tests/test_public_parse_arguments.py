from pytest_watcher import parse

def test_parse_args_fake_strict(monkeypatch):
    # change input arg defaults for different data
    args = ["--strict", "--color", "always"]
    parsed = parse.parse_args(args)
    assert parsed.strict is True
    assert parsed.color == "always"