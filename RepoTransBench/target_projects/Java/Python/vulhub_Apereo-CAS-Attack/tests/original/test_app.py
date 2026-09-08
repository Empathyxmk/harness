import io
import sys
import pytest

from src.vulhub.app import main, perform_attack


def run_main_and_capture(args):
    """
    Helper to capture stdout output of main().
    Returns the output string.
    """
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        main(args)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()

def test_main_no_args():
    out = run_main_and_capture([])
    assert "Hello from Apereo CAS Attack tool!" in out

def test_main_attack_cas_target():
    out = run_main_and_capture(['attack', 'cas-server'])
    assert "Simulating CAS attack on cas-server" in out

def test_main_attack_noncas_target():
    # "notcas" contains "cas", so is treated as CAS server, just like in Java.
    out = run_main_and_capture(['attack', 'notcas'])
    assert "Simulating CAS attack on notcas" in out

def test_main_attack_no_target():
    out = run_main_and_capture(['attack'])
    assert "No target specified for attack." in out

def test_main_help():
    out = run_main_and_capture(['help'])
    assert "Usage: java -jar apereo-cas-attack.jar" in out

def test_main_unknown_command():
    out = run_main_and_capture(['unknown'])
    assert "Unknown command: unknown" in out
    assert "Usage: java -jar apereo-cas-attack.jar" in out

def test_perform_attack_null():
    assert perform_attack(None) == "No target specified for attack."

def test_perform_attack_cas_target():
    assert perform_attack("cas-server") == "Simulating CAS attack on cas-server"

def test_perform_attack_noncas_target():
    # "something" does not contain "cas", so not a CAS server
    assert perform_attack("something") == "Target is not a CAS server: something"

def test_perform_attack_cas_substring_case_insensitive():
    # "bestcASattack" does NOT contain "cas" (lowercase), so not CAS server
    assert perform_attack("bestcASattack") == "Target is not a CAS server: bestcASattack"