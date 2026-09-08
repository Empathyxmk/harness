package com.scottyab.aescrypt;

import org.junit.Test;
import static org.junit.Assert.*;

import java.security.GeneralSecurityException;

public class AESCryptPublicTest {

    @Test
    public void testEncryptDecryptWithDifferentDataPublic() throws Exception {
        String password = "321secret";
        String message = "Public AESCrypt test 42.";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals("Public test value mismatch", message, decryptedMsg);
    }

    @Test
    public void testDecryptPrecomputedCiphertextPublic() throws Exception {
        String password = "public123";
        // This ciphertext is "helloPublic" encrypted with password "public123" using the AESCrypt implementation.
        String encryptedMsg = "Ru4RNkDqQboiRkHi7U0koA==";
        String result = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals("helloPublic", result);
    }

    @Test
    public void testEncryptDecryptEmptyStringPublic() throws Exception {
        String password = "emptyCase";
        String message = "";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals(message, decryptedMsg);
    }

    @Test
    public void testEncryptDecryptWithSpecialCharactersPublic() throws Exception {
        String password = "specialP@sswørd";
        String message = "!@#$%^&*()_+-=[]{};':,.<>/?`~";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals(message, decryptedMsg);
    }

    @Test
    public void testDecryptFailWithWrongPasswordPublic() throws Exception {
        String password = "correctPassword";
        String wrongPassword = "incorrectPassword";
        String message = "Mismatch password public";
        String encrypted = AESCrypt.encrypt(password, message);
        try {
            AESCrypt.decrypt(wrongPassword, encrypted);
            fail("Should throw GeneralSecurityException for wrong password");
        } catch (GeneralSecurityException e) {
            // expected behavior
        }
    }

}