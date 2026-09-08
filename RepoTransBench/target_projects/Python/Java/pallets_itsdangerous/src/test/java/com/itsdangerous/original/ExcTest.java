package com.itsdangerous.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.exc.*;

import java.util.HashMap;

public class ExcTest {

    @Test
    public void testBadData() {
        BadData exc = new BadData("bad data!");
        assertEquals("bad data!", exc.getMessage());
        assertNull(((BadData)exc).message == null ? null : exc.message);
    }

    @Test
    public void testBadSignaturePayload() {
        BadSignature bs = new BadSignature("msg", "mypayload");
        assertEquals("msg", bs.getMessage());
        assertEquals("mypayload", bs.payload);
    }

    @Test
    public void testBadTimeSignature() {
        BadTimeSignature bts = new BadTimeSignature("badtimesig", "foo", 1234L);
        assertEquals("badtimesig", bts.getMessage());
        assertEquals("foo", bts.payload);
        assertEquals(1234L, bts.dateSigned);
    }

    @Test
    public void testSignatureExpired() {
        SignatureExpired ex = new SignatureExpired("expired");
        assertEquals("expired", ex.getMessage());
        SignatureExpired ex2 = new SignatureExpired("expired2", "datahere");
        assertEquals("expired2", ex2.getMessage());
        assertEquals("datahere", ex2.payload);
    }

    @Test
    public void testBadHeaderInit() {
        HashMap<String, Object> header = new HashMap<>();
        header.put("alg", "none");
        Exception orig = new Exception("Not real error");
        BadHeader exc = new BadHeader("bad header error", "payload", header, orig);
        assertEquals("bad header error", exc.getMessage());
        assertEquals(header, exc.header);
        assertEquals(orig, exc.originalError);
        assertEquals("payload", exc.payload);
    }

    @Test
    public void testBadPayloadInit() {
        Exception orig = new Exception("Failed decode");
        BadPayload exc = new BadPayload("bad payload error", orig);
        assertEquals("bad payload error", exc.getMessage());
        assertEquals(orig, exc.originalError);
    }
}