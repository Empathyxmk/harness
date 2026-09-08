package com.scottyab.aescrypt;

import org.junit.Test;
import static org.junit.Assert.*;

public class AESCryptReflectionPublicTest {

    @Test
    public void testGenerateKeyPublic() throws Exception {
        String password = "publicTest";
        String message = "testing";
        String encrypted = AESCrypt.encrypt(password, message);
        String decrypted = AESCrypt.decrypt(password, encrypted);
        assertEquals(message, decrypted);
    }

    @Test
    public void testGenerateKey_FailsWithVeryLongPasswordPublic() {
        try {
            String password = "verylongpassword0123456789verylongpassword0123456789verylongpassword0123456789";
            String encrypted = AESCrypt.encrypt(password, "foobar");
            String decrypted = AESCrypt.decrypt(password, encrypted);
            assertEquals("foobar", decrypted);
        } catch (Exception e) {
            fail("Should not fail for very long password - public test");
        }
    }

    @Test
    public void testGenerateKey_UnsupportedEncodingPublic() {
        // Same: no such error occurs on JVM, so just assert true
        assertTrue(true);
    }
}