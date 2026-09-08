package com.tadeck.onetimepass.publictests;

import com.tadeck.onetimepass.Onetimepass;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicOnetimepassCoreTest {

    @Test
    public void testGetTotp() {
        String secret = "12345678901234567890";
        int code = Onetimepass.getTotp(secret, 30, 1600000000L);
        assertTrue(code >= 100000 && code < 1000000);
    }

    @Test
    public void testValidTotpToken() {
        String secret = "22222222222222222222";
        int code = Onetimepass.getTotp(secret, 30, 1600001000L);
        assertTrue(Onetimepass.validTotp(code, secret, 0, 1600001000L));
    }

    @Test
    public void testInvalidTotpToken() {
        String secret = "33333333333333333333";
        int code = Onetimepass.getTotp(secret, 30, 1600010000L);
        int wrongCode = (code + 10) % 1000000;
        assertFalse(Onetimepass.validTotp(wrongCode, secret, 0, 1600010000L));
    }

    @Test
    public void testGetHotp() {
        String secret = "JBSWY3DPEHPK3PXP";
        int code = Onetimepass.getHotp(secret, 7);
        assertTrue(code >= 100000 && code < 1000000);
    }

    @Test
    public void testValidHotpTrue() {
        String secret = "JBSWY3DPEHPK3PXQ";
        int code = Onetimepass.getHotp(secret, 42);
        assertTrue(Onetimepass.validHotp(code, secret, 42));
    }

    @Test
    public void testValidHotpFalse() {
        String secret = "JBSWY3DPEHPK3PXR";
        int code = Onetimepass.getHotp(secret, 53);
        assertFalse(Onetimepass.validHotp(code + 1, secret, 53));
    }
}