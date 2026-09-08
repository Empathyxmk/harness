import pytest

class TestPublicSoftware(object):
    @pytest.fixture(autouse=True)
    def init(self, ssh_audit):
        self.ssh = ssh_audit.SSH

    def test_unknown_software(self):
        ps = lambda x: self.ssh.Software.parse(self.ssh.Banner.parse(x))
        assert ps('SSH-1.4') is None
        assert ps('SSH-1.99-NotAServer') is None
        assert ps('SSH-2.0-FakeSSHd 3.1.4') is None

    def test_openssh_software(self):
        ps = lambda x: self.ssh.Software.parse(self.ssh.Banner.parse(x))
        # common
        s = ps('SSH-2.0-OpenSSH_6.9')
        assert s.vendor is None
        assert s.product == 'OpenSSH'
        assert s.version == '6.9'
        assert s.patch is None
        assert s.os is None
        assert str(s) == 'OpenSSH 6.9'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == str(s)
        assert repr(s) == '<Software(product=OpenSSH, version=6.9)>'
        # common, portable
        s = ps('SSH-2.0-OpenSSH_8.1p2')
        assert s.vendor is None
        assert s.product == 'OpenSSH'
        assert s.version == '8.1'
        assert s.patch == 'p2'
        assert s.os is None
        assert str(s) == 'OpenSSH 8.1p2'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == 'OpenSSH 8.1'
        assert repr(s) == '<Software(product=OpenSSH, version=8.1, patch=p2)>'
        # dot instead of underline
        s = ps('SSH-2.0-OpenSSH.7.4')
        assert s.vendor is None
        assert s.product == 'OpenSSH'
        assert s.version == '7.4'
        assert s.patch is None
        assert s.os is None
        assert str(s) == 'OpenSSH 7.4'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == str(s)
        assert repr(s) == '<Software(product=OpenSSH, version=7.4)>'
        # dash instead of underline
        s = ps('SSH-2.0-OpenSSH-4.8p2')
        assert s.vendor is None
        assert s.product == 'OpenSSH'
        assert s.version == '4.8'
        assert s.patch == 'p2'
        assert s.os is None
        assert str(s) == 'OpenSSH 4.8p2'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == 'OpenSSH 4.8'
        assert repr(s) == '<Software(product=OpenSSH, version=4.8, patch=p2)>'
        # patch prefix with dash
        s = ps('SSH-2.0-OpenSSH_8.2-custom')
        assert s.vendor is None
        assert s.product == 'OpenSSH'
        assert s.version == '8.2'
        assert s.patch == 'custom'
        assert s.os is None
        assert str(s) == 'OpenSSH 8.2 (custom)'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == 'OpenSSH 8.2'
        assert repr(s) == '<Software(product=OpenSSH, version=8.2, patch=custom)>'
        # patch prefix with underline
        s = ps('SSH-1.5-OpenSSH_5.5.5_hpn9v22')
        assert s.vendor is None
        assert s.product == 'OpenSSH'
        assert s.version == '5.5.5'
        assert s.patch == 'hpn9v22'
        assert s.os is None
        assert str(s) == 'OpenSSH 5.5.5 (hpn9v22)'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == 'OpenSSH 5.5.5'
        assert repr(s) == '<Software(product=OpenSSH, version=5.5.5, patch=hpn9v22)>'
        # patch prefix with dot
        s = ps('SSH-2.0-OpenSSH_8.5.ALPHA')
        assert s.vendor is None
        assert s.product == 'OpenSSH'
        assert s.version == '8.5'
        assert s.patch == 'ALPHA'
        assert s.os is None
        assert str(s) == 'OpenSSH 8.5 (ALPHA)'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == 'OpenSSH 8.5'
        assert repr(s) == '<Software(product=OpenSSH, version=8.5, patch=ALPHA)>'

    def test_dropbear_software(self):
        ps = lambda x: self.ssh.Software.parse(self.ssh.Banner.parse(x))
        # common
        s = ps('SSH-2.0-dropbear_2020.80')
        assert s.vendor is None
        assert s.product == 'Dropbear SSH'
        assert s.version == '2020.80'
        assert s.patch is None
        assert s.os is None
        assert str(s) == 'Dropbear SSH 2020.80'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == str(s)
        assert repr(s) == '<Software(product=Dropbear SSH, version=2020.80)>'
        # common, patch
        s = ps('SSH-2.0-dropbear_0.44alpha9')
        assert s.vendor is None
        assert s.product == 'Dropbear SSH'
        assert s.version == '0.44'
        assert s.patch == 'alpha9'
        assert s.os is None
        assert str(s) == 'Dropbear SSH 0.44 (alpha9)'
        assert str(s) == s.display()
        assert s.display(True) == str(s)
        assert s.display(False) == 'Dropbear SSH 0.44'
        assert repr(s) == '<Software(product=Dropbear SSH, version=0.44, patch=alpha9)>'