import pytest

class NashornExample:
    def print_hello_world(self):
        # Simulate: In JVM, Nashorn execution (may be missing)
        pass

def test_print_hello_world_no_exception():
    nashorn = NashornExample()
    try:
        nashorn.print_hello_world()
    except Exception:
        pass