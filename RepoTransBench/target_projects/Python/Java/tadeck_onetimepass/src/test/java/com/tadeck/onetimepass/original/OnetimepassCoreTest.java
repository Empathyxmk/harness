package com.tadeck.onetimepass.original;

import com.tadeck.onetimepass.Onetimepass;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.function.Executable;

import java.util.Base64;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class OnetimepassCoreTest {

    // Helper for monkeypatching time
    private void setMockTime(long fakeEpochSeconds) {
        // If Onetimepass uses System.currentTimeMillis()/1000L
        Onetimepass.setTimeProvider(() -> fakeEpochSeconds);
    }

    @Test
    public void testIsPossibleTokenAcceptsValidAndInvalid() {
        assertTrue(Onetimepass.isPossibleToken(123456));
        assertTrue(Onetimepass.isPossibleToken("123456".getBytes())); // bytes
        assertTrue(Onetimepass.isPossibleToken("123456"));
        assertFalse(Onetimepass.isPossibleToken("abcdef".getBytes()));
        assertFalse(Onetimepass.isPossibleToken("12345678".getBytes()));
        assertFalse(Onetimepass.isPossibleToken("")); // empty string
    }

    @Test
    public void testGetHotpTokenLengthAndInvalidSecret() {
        byte[] secret = "MFRGGZDFMZTWQ2LK".getBytes();
        Object result = Onetimepass.getHotp(secret, 10, 8, true);
        assertTrue(result instanceof String || result instanceof byte[]);
        int len = (result instanceof String)
                ? ((String) result).length() : ((byte[]) result).length;
        assertEquals(8, len);

        // invalid secret - should throw IllegalArgumentException, mimicking binascii.Error
        assertThrows(IllegalArgumentException.class, () -> {
            Onetimepass.getHotp("invalid!!!!".getBytes(), 1);
        });
    }

    @Test
    public void testGetHotpCasefoldFalse() {
        byte[] secret = "mfrggzdfmztwq2lk".getBytes();
        Object result = Onetimepass.getHotp(secret, 1, false);
        assertNotNull(result);

        // With casefold false, expect IllegalArgumentException, mimicking binascii.Error
        assertThrows(IllegalArgumentException.class, () -> {
            Onetimepass.getHotp(secret, 1, false);
        });
    }

    @Test
    public void testTotpDefault() {
        byte[] secret = "MFRGGZDFMZTWQ2LK".getBytes();
        Object token = Onetimepass.getTotp(secret);
        assertTrue(token instanceof Integer);

        // Test for fixed (mocked) time
        long fakeTime = 1650000000L;
        setMockTime(fakeTime);

        Object token1 = Onetimepass.getTotp(secret);
        assertTrue(token1 instanceof Integer);
    }

    @Test
    public void testValidHotpAndLast() {
        byte[] secret = "MFRGGZDFMZTWQ2LK".getBytes();
        int token = (int) Onetimepass.getHotp(secret, 2);
        assertEquals(2, Onetimepass.validHotp(token, secret));
        assertFalse(Onetimepass.validHotp(token, secret, 2));

        assertFalse(Onetimepass.validHotp("abcdef", secret));

        assertThrows(IllegalArgumentException.class, () -> {
            Onetimepass.validHotp(token, "invalidsecret!!!!!".getBytes());
        });
    }

    @Test
    public void testGetTotpTokenLengthAndString() {
        byte[] secret = "MFRGGZDFMZTWQ2LK".getBytes();
        long fakeTime = 1650000000L;
        setMockTime(fakeTime);

        Object result = Onetimepass.getTotp(secret, 8, true);
        assertTrue(result instanceof String || result instanceof byte[]);
        int len = (result instanceof String)
                ? ((String) result).length() : ((byte[]) result).length;
        assertEquals(8, len);
    }

    @Test
    public void testValidTotpAndWindow() {
        byte[] secret = "MFRGGZDFMZTWQ2LK".getBytes();
        long fakeTime = 1650000000L;
        setMockTime(fakeTime);

        int token = (int) Onetimepass.getTotp(secret);
        assertTrue(Onetimepass.validTotp(token, secret));
        assertTrue(Onetimepass.validTotp(token, secret, 1));
        assertFalse(Onetimepass.validTotp(token + 1, secret));
        assertFalse(Onetimepass.validTotp("abcdef", secret));
        assertThrows(IllegalArgumentException.class, () -> {
            Onetimepass.validTotp(token, "invalidsecret!!!".getBytes());
        });
    }

    @Test
    public void testGetTotpFixedTime() {
        byte[] secret = "MFRGGZDFMZTWQ2LK".getBytes();
        long fakeTime = 1000L;
        setMockTime(fakeTime);

        Object token = Onetimepass.getTotp(secret);
        assertTrue(token instanceof Integer);
    }
}