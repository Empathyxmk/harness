import pytest

def from_module(ssh_audit):
    return ssh_audit.Version

def test_public_compare_simple(ssh_audit):
    v = from_module(ssh_audit)
    assert v.compare('2.4.6', '2.4.6') == 0
    assert v.compare('1.8.0', '2.0.0') < 0
    assert v.compare('3.7.2', '2.9.5') > 0

def test_public_compare_suffix_patch(ssh_audit):
    v = from_module(ssh_audit)
    assert v.compare('2.4p8', '2.4p7') > 0
    assert v.compare('2.4beta2', '2.4beta3') < 0

def test_public_compare_empty_and_alpha(ssh_audit):
    v = from_module(ssh_audit)
    assert v.compare('2.2', '') > 0
    assert v.compare('', '0.0') < 0
    assert v.compare('2.2.1', '2.2alpha1') > 0