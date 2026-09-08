import pytest

class Benchmark:
    @staticmethod
    def main(args):
        if not args:
            raise RuntimeError("Usage")
        if "--foo" in args:
            raise RuntimeError("Unrecognized arg '--foo'. Usage")
        return "OK"

def test_main_with_no_args_throws_runtime_error():
    with pytest.raises(RuntimeError) as ex:
        Benchmark.main([])
    assert "Usage" in str(ex.value)