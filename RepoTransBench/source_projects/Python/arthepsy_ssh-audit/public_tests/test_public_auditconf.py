import pytest

def test_public_auditconf_defaults(ssh_audit):
    AuditConf = ssh_audit.AuditConf
    conf = AuditConf('testdomain', 22022)
    assert conf.host == 'testdomain'
    assert conf.port == 22022
    assert conf.colors is True
    assert conf.batch is False
    assert conf.verbose is False
    assert conf.ssh1 is True
    assert conf.ssh2 is True
    assert conf.level == 'info'

def test_public_auditconf_fields_mutation(ssh_audit):
    AuditConf = ssh_audit.AuditConf
    conf = AuditConf('hostabc', 1222)
    conf.colors = False
    conf.batch = True
    conf.verbose = True
    conf.ssh1 = False
    conf.ssh2 = True
    conf.level = 'fail'
    assert conf.colors is False
    assert conf.batch is True
    assert conf.verbose is True
    assert conf.ssh1 is False
    assert conf.ssh2 is True
    assert conf.level == 'fail'