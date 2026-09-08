package com.tadeck.onetimepass.original;

import com.tadeck.onetimepass.Onetimepass;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.security.MessageDigest;

import static org.junit.jupiter.api.Assertions.*;

public class OnetimepassExtraTest {

    private byte[] secret;

    @BeforeEach
    public void setUp() {
        secret = "MFRGGZDFMZTWQ2LK".getBytes();
    }

    @Test
    public void testGetHotpInvalidSecretType() {
        // Pass int instead of bytes - should throw ClassCastException/IllegalArgumentException
        assertThrows(ClassCastException.class, () -> {
            Onetimepass.getHotp((Object) 1234, 1);
        });
    }

    @Test
    public void testGetHotpIncorrectBase32() {
        // Not decodable base32 string: should raise IllegalArgumentException
        assertThrows(IllegalArgumentException.class, () -> {
            Onetimepass.getHotp("notbase32@#$".getBytes(), 1);
        });
    }

    @Test
    public void testGetHotpCustomDigest() throws Exception {
        // Java: Use SHA-256
        MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
        int val = Onetimepass.getHotp(secret, 1, sha256, 8);
        assertTrue(val >= 0);
        assertTrue(Integer.toString(val).length() <= 8);
    }

    @Test
    public void testGetHotpStringTypes() {
        String secretString = "MFRGGZDFMZTWQ2LK";
        Object res = Onetimepass.getHotp(secretString, 2, true);
        assertEquals("816065", res);
    }

    @Test
    public void testValidHotpReturnsFalse() {
        assertFalse(Onetimepass.validHotp(111111, secret, 0, 1));
    }

    @Test
    public void testValidHotpWithRange() {
        int tok = Onetimepass.getHotp(secret, 99);
        assertEquals(99, Onetimepass.validHotp(tok, secret, 97, 3));
    }

    @Test
    public void testValidTotpFalse() {
        assertFalse(Onetimepass.validTotp(123456, secret));
    }

    @Test
    public void testGetTotpAndValidTotp() {
        int tok = Onetimepass.getTotp(secret);
        assertTrue(Onetimepass.validTotp(tok, secret));
        assertFalse(Onetimepass.validTotp(tok + 1, secret));
    }

    @Test
    public void testGetTotpCustomTokenLength() {
        int tok = Onetimepass.getTotp(secret, 8);
        assertTrue(tok >= 0);
        assertTrue(Integer.toString(tok).length() <= 8);
    }
}