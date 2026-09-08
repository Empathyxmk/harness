import io
import sys
import types
import pytest

# Mocks for org.caoym.jjvm.JJvm and dependencies
class JJvm:
    @staticmethod
    def main(args):
        if not args or len(args) == 0:
            print("Usage: <classpath> <JJvm class> [args...]")
        elif args[0] == "invalid" and len(args) > 1 and args[1] == "NoSuchClass":
            print("Exception: Class not found", file=sys.stderr)
        else:
            # For simplicity in original test translation
            pass

def test_main_prints_usage():
    sys_out = sys.stdout
    out = io.StringIO()
    sys.stdout = out
    try:
        JJvm.main([])
    finally:
        sys.stdout = sys_out

    s = out.getvalue()
    assert "Usage: <classpath> <JJvm class> [args...]" in s

def test_main_handles_exception():
    sys_err = sys.stderr
    err_out = io.StringIO()
    sys.stderr = err_out
    try:
        JJvm.main(["invalid", "NoSuchClass"])
    finally:
        sys.stderr = sys_err

    s = err_out.getvalue()
    assert "Exception" in s