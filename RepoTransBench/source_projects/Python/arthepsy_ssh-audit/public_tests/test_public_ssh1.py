import pytest

class TestPublicSSH1:
    @pytest.fixture(autouse=True)
    def _init(self, ssh_audit):
        self.ssh = ssh_audit.SSH

    def test_message_id_names(self):
        SSH1 = self.ssh.SSH1
        # Use a different range than original for public test
        assert SSH1.MSGID.get(30) == "SSH_CMSG_X11_REQUEST_FORWARDING"
        assert SSH1.MSGID.get(10) == "SSH_SMSG_PUBLIC_KEY"
        assert SSH1.MSGID.get(50) == "SSH_CMSG_PORT_FORWARD_REQUEST"
        assert SSH1.MSGID.get(60, "foo") == "foo"