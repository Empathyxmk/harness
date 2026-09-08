import pytest
from click.testing import CliRunner
from pynubank.cli import main

def test_cli_help_public():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Usage:" in result.output or "usage:" in result.output

def test_cli_version_public():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert "pynubank" in result.output

def test_cli_invalid_command_public():
    runner = CliRunner()
    result = runner.invoke(main, ['invalidcmd'])
    assert result.exit_code != 0
    assert "No such command" in result.output or "no such command" in result.output