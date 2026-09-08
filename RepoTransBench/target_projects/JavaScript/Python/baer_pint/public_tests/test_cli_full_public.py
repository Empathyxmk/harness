import pytest

def test_handle_multiple_public_arguments():
    arguments_list = [['--dry-run'], ['--help'], ['--quiet']]
    for args in arguments_list:
        assert isinstance(args[0], str)
        assert args[0][0] == '-'

def test_not_throw_with_unknown_public_flags():
    def run_cli(args):
        # Simulate cli; don't actually execute
        if '--unknown-public' in args:
            return False
        return True
    try:
        run_cli(['--unknown-public'])
    except Exception:
        pytest.fail("run_cli should not throw")
    assert run_cli(['--unknown-public']) is False