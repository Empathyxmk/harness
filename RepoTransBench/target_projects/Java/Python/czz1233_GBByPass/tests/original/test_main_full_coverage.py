import io
from src.company import main

def test_main_with_no_args(capsys):
    main.main([])
    out = capsys.readouterr().out
    assert len(out) > 0

def test_main_with_normal_arg(capsys):
    main.main(["4567"])
    out = capsys.readouterr().out
    assert len(out) > 0

def test_main_with_alpha_arg(capsys):
    main.main(["abc123"])
    out = capsys.readouterr().out
    assert len(out) > 0

def test_main_with_empty_arg(capsys):
    main.main([""])
    out = capsys.readouterr().out
    assert len(out) > 0