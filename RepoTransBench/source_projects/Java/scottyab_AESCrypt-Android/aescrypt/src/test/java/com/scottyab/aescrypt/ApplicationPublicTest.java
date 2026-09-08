package com.scottyab.aescrypt;

import org.junit.Test;
import static org.junit.Assert.*;

import java.security.GeneralSecurityException;

public class ApplicationPublicTest {

    @Test
    public void testEncryptDecryptPublic() {
        String password = "anotherSecret";
        String message = "public test string!";

        if (AESCrypt.DEBUG_LOG_ENABLED) {
            AESCrypt.DEBUG_LOG_ENABLED = true;
        }

        String encryptedMsg = null;
        try {
            encryptedMsg = AESCrypt.encrypt(password, message);
        } catch (GeneralSecurityException e) {
            fail("error occurred during encrypt in public test");
        }

        String messageAfterDecrypt = null;
        try {
            messageAfterDecrypt = AESCrypt.decrypt(password, encryptedMsg);
        } catch (GeneralSecurityException e) {
            fail("error occurred during decrypt in public test");
        }

        assertEquals("messages don't match after encrypt and decrypt in public test", message, messageAfterDecrypt);
    }

    @Test
    public void testEncryptPublic() {
        String password = "publicPass";
        String message = "anotherMessage";

        try {
            String encryptedMsg = AESCrypt.encrypt(password, message);
            assertNotNull("encryptedMsg should not be null", encryptedMsg);
        } catch (GeneralSecurityException e) {
            fail("error occurred during encrypt in public test");
        }
    }

    @Test
    public void testDecryptPublic() {
        String password = "somePassword";
        // Encrypted "testOne" with password "somePassword"
        String encryptedMsg = "i5OSk38FnX6OGv5CeXf2iA==";
        try {
            String result = AESCrypt.decrypt(password, encryptedMsg);
            assertEquals("testOne", result);
        } catch (GeneralSecurityException e) {
            fail("error occurred during decrypt in public test");
        }
    }
}