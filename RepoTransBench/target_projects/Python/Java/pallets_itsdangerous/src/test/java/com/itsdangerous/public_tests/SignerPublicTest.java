package com.itsdangerous.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.Signer;
import com.itsdangerous.BadSignature;

public class SignerPublicTest {

    @Test
    public void testSignUnsign() {
        Signer s = new Signer("sign-key");
        byte[] msg = "tokentest".getBytes();
        byte[] signed = s.sign(msg);
        assertNotNull(signed);
        byte[] unsigned = s.unsign(signed);
        assertArrayEquals(msg, unsigned);
    }

    @Test
    public void testInvalidUnsignThrows() {
        Signer s = new Signer("sign-key");
        byte[] msg = "abc".getBytes();
        byte[] signed = s.sign(msg);
        signed[signed.length - 1] = '!';
        assertThrows(BadSignature.class, () -> s.unsign(signed));
    }
}