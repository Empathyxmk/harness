import pytest

class TestPublicBanner:
    @pytest.fixture(autouse=True)
    def _init(self, ssh_audit):
        self.ssh = ssh_audit.SSH

    def test_banner_parse(self):
        Banner = self.ssh.Banner
        b = Banner.parse('SSH-3.0-TestSSH_8.1')
        assert b is not None
        assert b.protocol == 3
        assert b.compat is None
        assert b.software == 'TestSSH_8.1'
        assert b.comments is None

        b2 = Banner.parse('SSH-2.0-FooSoftware_9.3 some-comment go')
        assert b2 is not None
        assert b2.protocol == 2
        assert b2.compat is None
        assert b2.software == 'FooSoftware_9.3'
        assert b2.comments == 'some-comment go'

    def test_banner_str_and_repr(self):
        Banner = self.ssh.Banner
        b = Banner.parse('SSH-3.0-PublicTest_2023 BetaX')
        assert str(b) == 'SSH-3.0-PublicTest_2023 BetaX'
        assert 'PublicTest_2023' in repr(b)