package com.itsdangerous.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.Signer;
import com.itsdangerous.BadSignature;

public class SignerTest {

    @Test
    public void testSignAndUnsign() {
        Signer s = new Signer("foo");
        byte[] msg = "bar".getBytes();
        byte[] signed = s.sign(msg);
        assertNotNull(signed);
        byte[] unsigned = s.unsign(signed);
        assertArrayEquals(msg, unsigned);
    }

    @Test
    public void testInvalidSignature() {
        Signer s = new Signer("foo");
        byte[] msg = "bar".getBytes();
        byte[] signed = s.sign(msg);
        // Tamper signature
        signed[signed.length - 1] = 'x';
        assertThrows(BadSignature.class, () -> s.unsign(signed));
    }

    @Test
    public void testSeparator() {
        Signer s = new Signer("foo", null, ":");
        assertEquals(":", s.getSep());
    }
}