package com.scottyab.aescrypt;

import org.junit.Before;
import org.junit.Test;

import javax.crypto.spec.SecretKeySpec;
import java.security.GeneralSecurityException;
import java.util.Base64;

import static org.junit.Assert.*;

public class AESCryptDebugTest {

    private static final String PASSWORD = "mypassword";
    private static final String MESSAGE = "test message for debug";
    private static final String ENCRYPTED;

    static {
        String tempEncrypted;
        try {
            tempEncrypted = AESCrypt.encrypt(PASSWORD, MESSAGE);
        } catch (Exception e) {
            tempEncrypted = null;
        }
        ENCRYPTED = tempEncrypted;
    }

    @Before
    public void enableDebug() {
        AESCrypt.DEBUG_LOG_ENABLED = true;
    }

    @Test
    public void testEncryptDecrypt_DebugLog_Enabled() throws Exception {
        // This hits if(DEBUG_LOG_ENABLED) branches in encrypt
        String encrypted = AESCrypt.encrypt(PASSWORD, MESSAGE);
        assertNotNull(encrypted);

        String decrypted = AESCrypt.decrypt(PASSWORD, encrypted);
        assertEquals(MESSAGE, decrypted);
    }

    @Test(expected = GeneralSecurityException.class)
    public void testEncrypt_InvalidAlgorithm_DebugLog() throws Exception {
        // Use a key with a wrong algorithm to trigger exception/throw
        SecretKeySpec badKey = new SecretKeySpec("1234567890123456".getBytes("UTF-8"), "BAD_ALGO");
        AESCrypt.encrypt(badKey, new byte[16], "hello".getBytes("UTF-8"));
    }

    @Test
    public void testDecrypt_InvalidBase64_DebugLog() {
        try {
            AESCrypt.decrypt(PASSWORD, "not-base64-***");
            fail("Should throw");
        } catch (GeneralSecurityException e) {
            // expected, triggers both DEBUG branches in decrypt
            assertNotNull(e);
        }
    }

    @Test(expected = GeneralSecurityException.class)
    public void testDecrypt_InvalidCipher_DebugLog() throws Exception {
        // Provide valid base64 that is not a valid cipher
        byte[] invalidBytes = "NotCipherText".getBytes("UTF-8");
        String invalidBase64 = Base64.getEncoder().encodeToString(invalidBytes);
        AESCrypt.decrypt(PASSWORD, invalidBase64);
    }
}