package com.scottyab.aescrypt;

import org.junit.Test;

import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import java.security.GeneralSecurityException;

import static org.junit.Assert.*;

public class AESCryptTest {

    @Test
    public void testBasicEncryptDecrypt() throws Exception {
        String password = "password";
        String message = "hello world";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals(message, decryptedMsg);
    }

    @Test
    public void testEncryptDecrypt_EmptyString() throws Exception {
        String password = "password";
        String message = "";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals(message, decryptedMsg);
    }

    @Test
    public void testEncryptDecrypt_NonAscii() throws Exception {
        String password = "password";
        String message = "こんにちは世界"; // "Hello World" in Japanese
        String encryptedMsg = AESCrypt.encrypt(password, message);
        String decryptedMsg = AESCrypt.decrypt(password, encryptedMsg);
        assertEquals(message, decryptedMsg);
    }

    @Test
    public void testDecrypt_WrongPassword() throws Exception {
        String password = "password";
        String wrongPassword = "notMyPassword";
        String message = "hello world";
        String encryptedMsg = AESCrypt.encrypt(password, message);
        try {
            AESCrypt.decrypt(wrongPassword, encryptedMsg);
            fail("Expected GeneralSecurityException");
        } catch (GeneralSecurityException e) {
            // expected
        }
    }

    @Test
    public void testDecrypt_InvalidBase64() throws Exception {
        String password = "password";
        String invalidBase64 = "not_base64!";
        try {
            AESCrypt.decrypt(password, invalidBase64);
            fail("Expected GeneralSecurityException");
        } catch (GeneralSecurityException e) {
            // expected
        }
    }

    @Test
    public void testDecrypt_InvalidData() throws Exception {
        String password = "password";
        // Clearly not a valid encrypted string
        String invalidData = "MTIzNA=="; // "1234" base64
        try {
            AESCrypt.decrypt(password, invalidData);
            fail("Expected GeneralSecurityException");
        } catch (GeneralSecurityException e) {
            // expected
        }
    }

    @Test(expected = NullPointerException.class)
    public void testEncryptDecrypt_NullPassword() throws Exception {
        String message = "hello";
        AESCrypt.encrypt(null, message);
    }

    @Test(expected = NullPointerException.class)
    public void testEncryptDecrypt_NullMessage() throws Exception {
        String password = "pw";
        AESCrypt.encrypt(password, null);
    }

    @Test
    public void testDirectEncryptDecrypt() throws Exception {
        String pw = "testing";
        String msg = "msg";
        String encrypted = AESCrypt.encrypt(pw, msg);
        String decrypted = AESCrypt.decrypt(pw, encrypted);
        assertEquals(msg, decrypted);
    }
}