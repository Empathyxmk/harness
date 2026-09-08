import pytest

def test_public_errors_valueerror(ssh_audit):
    errors = ssh_audit.Errors
    with pytest.raises(ValueError):
        raise errors.FailError('fail in public')

def test_public_errors_sockerror(ssh_audit):
    errors = ssh_audit.Errors
    ex = errors.SockError('Socket error for public!')
    assert str(ex) == 'Socket error for public!'

def test_public_errors_connerror(ssh_audit):
    errors = ssh_audit.Errors
    ex = errors.ConnError('Connection down in public.')
    assert str(ex) == 'Connection down in public.'