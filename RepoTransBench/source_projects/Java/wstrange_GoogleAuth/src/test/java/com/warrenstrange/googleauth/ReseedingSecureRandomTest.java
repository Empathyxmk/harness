package com.warrenstrange.googleauth;

import org.junit.Test;

import java.lang.reflect.Field;
import java.util.Arrays;

import static org.junit.Assert.*;

public class ReseedingSecureRandomTest {

    @Test
    public void testDefaultConstructorAndNextBytes() {
        ReseedingSecureRandom random = new ReseedingSecureRandom();
        byte[] bytes = new byte[10];
        random.nextBytes(bytes);
        // Can't predict, but we know it fills with non-defaults
        assertNotNull(bytes);
        assertTrue(bytes.length > 0);
    }

    @Test
    public void testConstructorWithAlgorithm() {
        ReseedingSecureRandom random = new ReseedingSecureRandom("SHA1PRNG");
        byte[] bytes = new byte[16];
        random.nextBytes(bytes);
        assertNotNull(bytes);
    }

    @Test
    public void testConstructorWithAlgorithmAndProvider_invalidProvider() {
        try {
            new ReseedingSecureRandom("SHA1PRNG", "FAKE_PROVIDER");
            fail("Expected GoogleAuthenticatorException for bad provider");
        } catch (GoogleAuthenticatorException e) {
            assertTrue(e.getMessage().contains("provider"));
        }
    }

    @Test
    public void testConstructorWithNullAlgorithm() {
        try {
            new ReseedingSecureRandom((String)null);
            fail("Expected IllegalArgumentException for null algorithm");
        } catch (IllegalArgumentException e) {
            // ok!
        }
    }

    @Test
    public void testConstructorWithNullProvider() {
        try {
            new ReseedingSecureRandom("SHA1PRNG", null);
            fail("Expected IllegalArgumentException for null provider");
        } catch (IllegalArgumentException e) {
            // ok!
        }
    }

    @Test
    public void testForceReseed() throws Exception {
        ReseedingSecureRandom random = new ReseedingSecureRandom();
        // Simulate crossing MAX_OPERATIONS by setting private count via reflection
        Field countField = ReseedingSecureRandom.class.getDeclaredField("count");
        countField.setAccessible(true);
        ((java.util.concurrent.atomic.AtomicInteger)countField.get(random)).set(1_000_001);

        byte[] bytes = new byte[5];
        random.nextBytes(bytes);
        assertNotNull(bytes);
    }
}