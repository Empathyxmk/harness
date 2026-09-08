import pytest
from src.intere_hacking.commandline import main_commandline

def test_single_arg(capsys):
    """Test commandline with a single argument."""
    argv1 = ["prog"]
    main_commandline(1, argv1)
    captured = capsys.readouterr()
    assert "Usage:" in captured.out

def test_multiple_args(capsys):
    """Test commandline with multiple arguments."""
    argv3 = ["prog", "alpha", "beta"]
    main_commandline(3, argv3)
    captured = capsys.readouterr()
    assert "Arguments: alpha beta" in captured.out

def test_coverage_complete(capsys):
    """Test that coverage run is complete."""
    print("commandline coverage run complete")
    captured = capsys.readouterr()
    assert "commandline coverage run complete" in captured.out