package com.scottyab.aescrypt;

import org.junit.Test;

import java.security.GeneralSecurityException;

import static org.junit.Assert.*;

public class AESCryptDebugPublicTest {

    @Test
    public void testEncryptDecryptWithDebugPublic() throws Exception {
        boolean oldDebug = AESCrypt.DEBUG_LOG_ENABLED;
        AESCrypt.DEBUG_LOG_ENABLED = true;
        String password = "pubDebugPass128";
        String message = "Debug public test message with 128";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals("Debug public message failed", message, decryptedMsg);
        AESCrypt.DEBUG_LOG_ENABLED = oldDebug;
    }

    @Test
    public void testWrongPasswordDecryptionPublic() {
        String password = "pubDebugPassword";
        String wrongPassword = "pubDebugWrongPwd";
        String message = "Different message for debug";
        try {
            String encryptedMsg = AESCrypt.encrypt(password, message);
            try {
                AESCrypt.decrypt(wrongPassword, encryptedMsg);
                fail("Expected exception for wrong password in debug public test");
            } catch (GeneralSecurityException e) {
                // expected
            }
        } catch (GeneralSecurityException e) {
            fail("Encrypt should not throw in debug public test: " + e.getMessage());
        }
    }

    @Test
    public void testEncryptDecryptWithUnicodePublic() throws Exception {
        String password = "Pública123!";
        String message = "Тестовое сообщение 🌍";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals("Unicode debug public message failed", message, decryptedMsg);
    }
}