package com.warrenstrange.googleauth;

import org.junit.Test;

import java.lang.reflect.Field;

import static org.junit.Assert.*;

public class ReseedingSecureRandomPublicTest {

    @Test
    public void testDefaultConstructorAndNextBytes_public() {
        ReseedingSecureRandom random = new ReseedingSecureRandom();
        byte[] bytes = new byte[12];
        random.nextBytes(bytes);
        assertNotNull(bytes);
        assertTrue(bytes.length == 12);
    }

    @Test
    public void testConstructorWithAlgorithm_public() {
        ReseedingSecureRandom random = new ReseedingSecureRandom("SHA1PRNG");
        byte[] bytes = new byte[8];
        random.nextBytes(bytes);
        assertNotNull(bytes);
        assertEquals(8, bytes.length);
    }

    @Test
    public void testConstructorWithAlgorithmAndProvider_invalidProvider_public() {
        try {
            new ReseedingSecureRandom("SHA1PRNG", "NON_EXISTENT_PROVIDER");
            fail("Expected GoogleAuthenticatorException for bad provider");
        } catch (GoogleAuthenticatorException e) {
            assertTrue(e.getMessage().toLowerCase().contains("provider"));
        }
    }

    @Test
    public void testConstructorWithNullAlgorithm_public() {
        try {
            new ReseedingSecureRandom((String)null);
            fail("Expected IllegalArgumentException for null algorithm");
        } catch (IllegalArgumentException e) {
            // expected!
        }
    }

    @Test
    public void testConstructorWithNullProvider_public() {
        try {
            new ReseedingSecureRandom("SHA1PRNG", null);
            fail("Expected IllegalArgumentException for null provider");
        } catch (IllegalArgumentException e) {
            // expected!
        }
    }

    @Test
    public void testForceReseed_public() throws Exception {
        ReseedingSecureRandom random = new ReseedingSecureRandom();
        // Set count via reflection to a higher value to simulate reseed trigger
        Field countField = ReseedingSecureRandom.class.getDeclaredField("count");
        countField.setAccessible(true);
        ((java.util.concurrent.atomic.AtomicInteger)countField.get(random)).set(2_000_001);

        byte[] bytes = new byte[7];
        random.nextBytes(bytes);
        assertNotNull(bytes);
        assertEquals(7, bytes.length);
    }
}