import re
import pytest

class TestPublicBuffer(object):
    @pytest.fixture(autouse=True)
    def init(self, ssh_audit):
        self.rbuf = ssh_audit.ReadBuf
        self.wbuf = ssh_audit.WriteBuf
        self.utf8rchar = b'\xef\xbf\xbd'

    @classmethod
    def _b(cls, v):
        v = re.sub(r'\s', '', v)
        data = [int(v[i * 2:i * 2 + 2], 16) for i in range(len(v) // 2)]
        return bytes(bytearray(data))

    def test_unread(self):
        w = self.wbuf().write_byte(10).write_int(99).write_flush()
        r = self.rbuf(w)
        assert r.unread_len == 5
        r.read_byte()
        assert r.unread_len == 4
        r.read_int()
        assert r.unread_len == 0

    def test_byte(self):
        w = lambda x: self.wbuf().write_byte(x).write_flush()
        r = lambda x: self.rbuf(x).read_byte()
        tc = [(0x02, '02'),
              (0xaa, 'aa'),
              (0x5f, '5f'),
              (0x7c, '7c')]
        for p in tc:
            assert w(p[0]) == self._b(p[1])
            assert r(self._b(p[1])) == p[0]

    def test_bool(self):
        w = lambda x: self.wbuf().write_bool(x).write_flush()
        r = lambda x: self.rbuf(x).read_bool()
        tc = [(True,  '01'),
              (False, '00')]
        for p in tc:
            assert w(p[0]) == self._b(p[1])
            assert r(self._b(p[1])) == p[0]

    def test_int(self):
        w = lambda x: self.wbuf().write_int(x).write_flush()
        r = lambda x: self.rbuf(x).read_int()
        tc = [(0x2a,       '00 00 00 2a'),
              (0x1234,     '00 00 12 34'),
              (0xabcd1234, 'ab cd 12 34'),
              (0x7fffffff, '7f ff ff ff')]
        for p in tc:
            assert w(p[0]) == self._b(p[1])
            assert r(self._b(p[1])) == p[0]

    def test_string(self):
        w = lambda x: self.wbuf().write_string(x).write_flush()
        r = lambda x: self.rbuf(x).read_string()
        tc = [(u'test9',  '00 00 00 05 74 65 73 74 39'),
              (b'fooB',  '00 00 00 04 66 6f 6f 42')]
        for p in tc:
            v = p[0]
            assert w(v) == self._b(p[1])
            if not isinstance(v, bytes):
                v = bytes(bytearray(v, 'utf-8'))
            assert r(self._b(p[1])) == v

    def test_list(self):
        w = lambda x: self.wbuf().write_list(x).write_flush()
        r = lambda x: self.rbuf(x).read_list()
        tc = [(['foo', 'bar', 'baz'], '00 00 00 0b 66 6f 6f 2c 62 61 72 2c 62 61 7a')]
        for p in tc:
            assert w(p[0]) == self._b(p[1])
            assert r(self._b(p[1])) == p[0]

    def test_list_nonutf8(self):
        r = lambda x: self.rbuf(x).read_list()
        src = self._b('00 00 00 04 fa ce be ef')
        # Ensures decode with replacement char
        dst = [(b'\xfa\xce' + self.utf8rchar + self.utf8rchar).decode('utf-8')]
        assert r(src) == dst

    def test_line(self):
        w = lambda x: self.wbuf().write_line(x).write_flush()
        r = lambda x: self.rbuf(x).read_line()
        tc = [(u'another line!', '61 6e 6f 74 68 65 72 20 6c 69 6e 65 21 0d 0a')]
        for p in tc:
            assert w(p[0]) == self._b(p[1])
            assert r(self._b(p[1])) == p[0]

    def test_line_nonutf8(self):
        r = lambda x: self.rbuf(x).read_line()
        src = self._b('fa ce be ac')
        dst = (b'\xfa\xce' + self.utf8rchar + self.utf8rchar).decode('utf-8')
        assert r(src) == dst

    def test_bitlen(self):
        class Py2StyleInt(int):
            def bit_length(self):
                raise AttributeError
        assert self.wbuf._bitlength(13) == 4
        assert self.wbuf._bitlength(Py2StyleInt(13)) == 4

    def test_mpint1(self):
        mpint1w = lambda x: self.wbuf().write_mpint1(x).write_flush()
        mpint1r = lambda x: self.rbuf(x).read_mpint1()
        tc = [(0x3,     '00 03'),
              (0x2345,  '00 11 23 45'),
              (0x54678, '00 13 05 46 78'),
              (0xc0ffee, '00 21 c0 ff ee')]
        for p in tc:
            assert mpint1w(p[0]) == self._b(p[1])
            assert mpint1r(self._b(p[1])) == p[0]