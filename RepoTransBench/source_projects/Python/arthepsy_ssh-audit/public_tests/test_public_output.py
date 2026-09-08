import pytest

def test_public_output_levels(ssh_audit, output_spy):
    Output = ssh_audit.Output
    out = Output()
    output_spy.begin()
    out.head('==PUBLIC-TEST-HEADER==')
    out.info('Some info level text')
    out.warn('A warning appears!')
    out.fail('Major fail here!')
    out.sep()
    lines = output_spy.flush()
    assert '==PUBLIC-TEST-HEADER==' in lines[0]
    assert any('Some info level text' in x for x in lines)
    assert any('A warning appears!' in x for x in lines)
    assert any('Major fail here!' in x for x in lines)

def test_public_output_batch(ssh_audit, output_spy):
    Output = ssh_audit.Output
    out = Output()
    out.batch = True
    output_spy.begin()
    out.info('batch info output')
    out.warn('batch warn output')
    out.fail('batch fail output')
    out.sep()
    lines = output_spy.flush()
    assert all('batch' in x for x in lines if x)