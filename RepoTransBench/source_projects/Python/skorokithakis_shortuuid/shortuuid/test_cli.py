import sys
import io
import uuid
from shortuuid import encode
import pytest

def test_cli_encode_and_decode(monkeypatch, capsys):
    from shortuuid import cli

    # Test encode
    args = ["encode", str(uuid.uuid4())]
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    cli.cli()
    out_encode = capsys.readouterr().out.strip()
    assert isinstance(out_encode, str)
    assert len(out_encode) > 0

    # Test decode (with string from encode)
    args = ["decode", out_encode]
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    cli.cli()
    out_decode = capsys.readouterr().out.strip()
    # Should be a UUID
    uuid.UUID(out_decode)

def test_cli_decode_legacy(monkeypatch, capsys):
    from shortuuid import cli
    u = uuid.uuid4()
    s = encode(u)
    args = ["decode", s[::-1], "--legacy"]
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    cli.cli()
    out = capsys.readouterr().out.strip()
    assert uuid.UUID(out)

def test_cli_no_fn(monkeypatch, capsys):
    from shortuuid import cli
    # No subcommand, just invokes uuid() and prints result
    args = []
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    cli.cli()
    outstr = capsys.readouterr().out.strip()
    assert isinstance(outstr, str)