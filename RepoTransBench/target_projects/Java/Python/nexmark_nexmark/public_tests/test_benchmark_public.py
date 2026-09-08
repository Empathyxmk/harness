import pytest

class Benchmark:
    @staticmethod
    def main(args):
        if args is None:
            raise RuntimeError("Usage")
        if "--foo" in (args or []):
            raise RuntimeError("Invalid arg")
        return "OK"

def test_main_with_null_args_throws_runtime_exception():
    with pytest.raises(RuntimeError) as ex:
        Benchmark.main(None)
    assert "usage" in str(ex.value).lower()

def test_main_with_invalid_args_throws_parse_exception_or_runtime():
    with pytest.raises(Exception) as ex:
        Benchmark.main(["--foo"])
    assert ex.value is not None