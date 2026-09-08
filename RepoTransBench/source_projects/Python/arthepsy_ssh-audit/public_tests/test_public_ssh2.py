import struct
import pytest

class TestPublicSSH2(object):
    @pytest.fixture(autouse=True)
    def init(self, ssh_audit):
        self.ssh = ssh_audit.SSH
        self.ssh2 = ssh_audit.SSH2
        self.rbuf = ssh_audit.ReadBuf
        self.wbuf = ssh_audit.WriteBuf
        self.audit = ssh_audit.audit
        self.AuditConf = ssh_audit.AuditConf

    def _conf(self):
        conf = self.AuditConf('publichost', 2022)
        conf.colors = False
        conf.batch = True
        conf.verbose = True
        conf.ssh1 = False
        conf.ssh2 = True
        return conf

    @classmethod
    def _create_ssh2_packet(cls, payload):
        padding = -(len(payload) + 5) % 8
        if padding < 4:
            padding += 8
        plen = len(payload) + padding + 1
        pad_bytes = b'\x00' * padding
        data = struct.pack('>Ib', plen, padding) + payload + pad_bytes
        return data

    def _simple_kex_payload(self):
        w = self.wbuf()
        w.write(b'\x12\x34\x56\x78\x90\xab\xcd\xef\x01\x23\x45\x67\x89\xab\xcd\xef')
        w.write_list([u'ecdh-sha2-nistp256', u'kex-dummy'])
        w.write_list([u'ssh-ed25519', u'dss-rsa'])
        w.write_list([u'aes128-cbc', u'aes256-cbc'])
        w.write_list([u'aes192-cbc', u'aes192-gcm'])
        w.write_list([u'hmac-sha2-256', u'sha1'])
        w.write_list([u'hmac-sha2-512', u'sha512'])
        w.write_list([u'zlib@openssh.com'])
        w.write_list([u'none'])
        w.write_list([u'key1'])
        w.write_list([u'key2'])
        w.write_byte(False)
        w.write_int(0)
        return w.write_flush()

    def test_public_kex_read(self):
        kex = self.ssh2.Kex.parse(self._simple_kex_payload())
        assert kex is not None
        assert kex.cookie == b'\x12\x34\x56\x78\x90\xab\xcd\xef\x01\x23\x45\x67\x89\xab\xcd\xef'
        assert kex.kex_algorithms == [u'ecdh-sha2-nistp256', u'kex-dummy']
        assert kex.key_algorithms == [u'ssh-ed25519', u'dss-rsa']
        assert kex.client is not None
        assert kex.server is not None
        assert kex.client.encryption == [u'aes128-cbc', u'aes256-cbc']
        assert kex.server.encryption == [u'aes192-cbc', u'aes192-gcm']
        assert kex.client.mac == [u'hmac-sha2-256', u'sha1']
        assert kex.server.mac == [u'hmac-sha2-512', u'sha512']
        assert kex.client.compression == [u'zlib@openssh.com']
        assert kex.server.compression == [u'none']
        assert kex.languages_client == [u'key1']
        assert kex.languages_server == [u'key2']
        assert kex.first_kex_packet_follows is False
        assert kex.reserved == 0