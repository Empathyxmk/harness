package com.tadeck.onetimepass.publictests;

import com.tadeck.onetimepass.Onetimepass;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicOnetimepassExtraTest {

    @Test
    public void testSecretToBase32() {
        byte[] secret = "different secret".getBytes();
        String b32 = Onetimepass.secretToBase32(secret);
        assertNotNull(b32);
        for (char c : b32.replace("=", "").toCharArray()) {
            assertTrue("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567".indexOf(c) >= 0);
        }
    }

    @Test
    public void testValidBase32ReturnTypes() {
        assertTrue(Onetimepass.validBase32("MFRGGZDFMZRW63LQ"));
        assertFalse(Onetimepass.validBase32("123#XYZ"));
    }

    @Test
    public void testGenerateNewSecretLength() {
        String secret8 = Onetimepass.generateNewSecret(8);
        String secret24 = Onetimepass.generateNewSecret(24);
        assertNotNull(secret8);
        assertNotNull(secret24);
        assertEquals(8, secret8.length());
        assertEquals(24, secret24.length());
    }

    @Test
    public void testGenerateNewSecretBase32() {
        String secret = Onetimepass.generateNewSecret(18);
        assertTrue(Onetimepass.validBase32(secret));
    }
}