import sys
import pytest

def test_cli_invalid_arguments(monkeypatch, capsys):
    from shortuuid import cli

    # Pass bogus command, should trigger argparse SystemExit
    args = ["bogus"]
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    with pytest.raises(SystemExit):
        cli.cli()

    # Fail 'encode' if no UUID
    args = ["encode"]
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    with pytest.raises(SystemExit):
        cli.cli()

    # Fail 'decode' if no shortuuid
    args = ["decode"]
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    with pytest.raises(SystemExit):
        cli.cli()