package com.sshaudit.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Arrays;
import java.nio.charset.StandardCharsets;

// NOTE: This class assumes stubs/mocks for ReadBuf, WriteBuf and utf8rchar available from testing context
public class TestBuffer {

    public static class ReadBuf {
        private byte[] buf;
        private int pos = 0;
        public int unread_len;

        public ReadBuf(byte[] input) {
            this.buf = input;
            this.pos = 0;
            this.unread_len = input.length;
        }
        public int read_byte() {
            int b = buf[pos] & 0xFF;
            pos += 1;
            unread_len -= 1;
            return b;
        }
        public boolean read_bool() {
            return read_byte() != 0;
        }
        public int read_int() {
            int v = ((buf[pos] & 0xFF) << 24) | ((buf[pos+1] & 0xFF) << 16) | 
                    ((buf[pos+2] & 0xFF) << 8) | ((buf[pos+3] & 0xFF));
            pos += 4;
            unread_len -= 4;
            return v;
        }
        public byte[] read_string() {
            int len = read_int();
            byte[] b = Arrays.copyOfRange(buf, pos, pos+len);
            pos += len;
            unread_len -= len;
            return b;
        }
        public String read_line() {
            int start = pos;
            while (pos < buf.length && !(buf[pos] == 0x0d && pos+1 < buf.length && buf[pos+1] == 0x0a)) {
                pos++;
            }
            String result = new String(Arrays.copyOfRange(buf, start, pos), StandardCharsets.UTF_8);
            pos += 2; // skip \r\n
            unread_len = buf.length - pos;
            return result;
        }
        public java.util.List<String> read_list() {
            int total = read_int();
            byte[] b = Arrays.copyOfRange(buf, pos, pos + total);
            pos += total;
            unread_len -= total;
            String listStr = new String(b, StandardCharsets.UTF_8);
            String[] parts = listStr.split(",");
            return Arrays.asList(parts);
        }
        public int read_mpint1() {
            // This is stub logic. In real code, would parse SSH MPINT format.
            if (buf.length == 2) {
                return ((buf[0]&0xFF) << 8) | (buf[1]&0xFF);
            }
            if (buf.length == 4) {
                return ((buf[2]&0xFF) << 8) | (buf[3]&0xFF);
            }
            // fallback
            return 0;
        }
    }

    public static class WriteBuf {
        private java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();

        public WriteBuf write_byte(int val) {
            baos.write(val & 0xFF);
            return this;
        }
        public WriteBuf write_bool(boolean b) {
            baos.write(b ? 1 : 0);
            return this;
        }
        public WriteBuf write_int(int val) {
            baos.write((val >>> 24) & 0xFF);
            baos.write((val >>> 16) & 0xFF);
            baos.write((val >>> 8) & 0xFF);
            baos.write((val) & 0xFF);
            return this;
        }
        public WriteBuf write_string(Object input) {
            byte[] b;
            if (input instanceof String) {
                b = ((String) input).getBytes(StandardCharsets.UTF_8);
            } else if (input instanceof byte[]) {
                b = (byte[]) input;
            } else {
                throw new IllegalArgumentException("unknown type");
            }
            write_int(b.length);
            baos.write(b, 0, b.length);
            return this;
        }
        public WriteBuf write_list(java.util.List<String> l) {
            String joined = String.join(",", l);
            write_int(joined.length());
            baos.write(joined.getBytes(StandardCharsets.UTF_8), 0, joined.length());
            return this;
        }
        public WriteBuf write_line(String l) {
            baos.write(l.getBytes(StandardCharsets.UTF_8), 0, l.length());
            baos.write('\r');
            baos.write('\n');
            return this;
        }
        public WriteBuf write_mpint1(int val) {
            // This is stub logic, real SSH MPINT logic differs.
            if (val <= 0xFFFF) {
                baos.write(((val >> 8) & 0xFF));
                baos.write(val & 0xFF);
            } else if (val <= 0xFFFFFF) {
                baos.write(((val >> 16) & 0xFF));
                baos.write(((val >> 8) & 0xFF));
                baos.write(val & 0xFF);
            } else {
                baos.write(((val >> 24) & 0xFF));
                baos.write(((val >> 16) & 0xFF));
                baos.write(((val >> 8) & 0xFF));
                baos.write(val & 0xFF);
            }
            return this;
        }
        public byte[] write_flush() {
            return baos.toByteArray();
        }
        public int _bitlength(int val) {
            if (val == 0) return 0;
            return 32 - Integer.numberOfLeadingZeros(val);
        }
    }

    private ReadBuf rbuf(byte[] input) { return new ReadBuf(input); }
    private WriteBuf wbuf() { return new WriteBuf(); }

    private static byte[] _b(String v) {
        v = v.replaceAll("\\s", "");
        byte[] data = new byte[v.length()/2];
        for (int i = 0; i < v.length()/2; i++) {
            data[i] = (byte) Integer.parseInt(v.substring(i*2, i*2+2), 16);
        }
        return data;
    }

    @Test
    public void test_unread() {
        WriteBuf w = wbuf().write_byte(1).write_int(2);
        byte[] wb = w.write_flush();
        ReadBuf r = rbuf(wb);
        assertEquals(5, r.unread_len);
        r.read_byte();
        assertEquals(4, r.unread_len);
        r.read_int();
        assertEquals(0, r.unread_len);
    }

    @Test
    public void test_byte() {
        Object[][] tc = new Object[][] {
            {0x00, "00"}, {0x01, "01"}, {0x10, "10"}, {0xff, "ff"}
        };
        for (Object[] p : tc) {
            byte[] expected = _b((String)p[1]);
            byte[] actual = wbuf().write_byte((int)p[0]).write_flush();
            assertArrayEquals(expected, actual);
            int got = rbuf(expected).read_byte();
            assertEquals(p[0], got);
        }
    }

    @Test
    public void test_bool() {
        Object[][] tc = new Object[][] {
            {true, "01"}, {false, "00"}
        };
        for (Object[] p : tc) {
            byte[] expected = _b((String)p[1]);
            byte[] actual = wbuf().write_bool((boolean)p[0]).write_flush();
            assertArrayEquals(expected, actual);
            boolean got = rbuf(expected).read_bool();
            assertEquals(p[0], got);
        }
    }

    @Test
    public void test_int() {
        Object[][] tc = new Object[][] {
            {0x00, "00 00 00 00"}, {0x01, "00 00 00 01"},
            {0xabcd, "00 00 ab cd"}, {0xffffffff, "ff ff ff ff"}
        };
        for (Object[] p : tc) {
            byte[] expected = _b((String)p[1]);
            byte[] actual = wbuf().write_int((int)p[0]).write_flush();
            assertArrayEquals(expected, actual);
            int got = rbuf(expected).read_int();
            assertEquals(p[0], got);
        }
    }

    @Test
    public void test_string() {
        Object[][] tc = new Object[][] {
            {"abc1", "00 00 00 04 61 62 63 31"},
            {new byte[]{'a','b','c','2'}, "00 00 00 04 61 62 63 32"}
        };
        for (Object[] p : tc) {
            Object v = p[0];
            byte[] expected = _b((String)p[1]);
            byte[] actual = wbuf().write_string(v).write_flush();
            assertArrayEquals(expected, actual);
            byte[] rVal = rbuf(expected).read_string();
            if (v instanceof byte[]) {
                assertArrayEquals((byte[])v, rVal);
            } else {
                assertArrayEquals(((String)v).getBytes(StandardCharsets.UTF_8), rVal);
            }
        }
    }

    @Test
    public void test_list() {
        Object[] p = new Object[] {
            java.util.Arrays.asList("d", "ef", "ault"), "00 00 00 09 64 2c 65 66 2c 61 75 6c 74"
        };
        byte[] expected = _b((String)p[1]);
        byte[] actual = wbuf().write_list((java.util.List<String>)p[0]).write_flush();
        assertArrayEquals(expected, actual);
        java.util.List<String> got = rbuf(expected).read_list();
        assertEquals(p[0], got);
    }

    @Test
    public void test_line() {
        Object[] p = new Object[] {
            "example line", "65 78 61 6d 70 6c 65 20 6c 69 6e 65 0d 0a"
        };
        byte[] expected = _b((String)p[1]);
        byte[] actual = wbuf().write_line((String)p[0]).write_flush();
        assertArrayEquals(expected, actual);
        String got = rbuf(expected).read_line();
        assertEquals(p[0], got);
    }

    static class Py26Int extends Number {
        private int value;
        Py26Int(int v) { this.value = v; }
        @Override public int intValue() { return value; }
        @Override public long longValue() { return value; }
        @Override public float floatValue() { return value; }
        @Override public double doubleValue() { return value; }
        public int bit_length() { throw new RuntimeException("AttributeError"); }
    }

    @Test
    public void test_bitlen() {
        WriteBuf w = wbuf();
        assertEquals(6, w._bitlength(42));
        assertEquals(6, w._bitlength(new Py26Int(42).intValue()));
    }
}