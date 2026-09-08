package com.warrenstrange.googleauth;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests for GoogleAuthenticatorConfig: constructor, getters, builder only (avoid non-existent setters).
 */
public class GoogleAuthenticatorConfigTest {

    @Test
    public void testDefaultConstructorAndGetters() {
        GoogleAuthenticatorConfig config = new GoogleAuthenticatorConfig();
        assertTrue(config.getWindowSize() >= 0);
        assertTrue(config.getCodeDigits() >= 0);
        assertNotNull(config.getKeyRepresentation());
        assertTrue(config.getTimeStepSizeInMillis() > 0);
        assertNotNull(config.getHmacHashFunction());
        assertTrue(config.getNumberOfScratchCodes() >= 0);
        assertTrue(config.getSecretBits() >= 0);
    }

    @Test
    public void testBuilder() {
        GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder builder =
                new GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder();
        builder.setWindowSize(4)
                .setCodeDigits(7)
                .setKeyRepresentation(KeyRepresentation.BASE64)
                .setTimeStepSizeInMillis(654321L)
                .setHmacHashFunction(HmacHashFunction.valueOf("HmacSHA1"))
                .setNumberOfScratchCodes(7)
                .setSecretBits(160);

        GoogleAuthenticatorConfig config = builder.build();

        assertEquals(4, config.getWindowSize());
        assertEquals(7, config.getCodeDigits());
        assertEquals(KeyRepresentation.BASE64, config.getKeyRepresentation());
        assertEquals(654321L, config.getTimeStepSizeInMillis());
        assertEquals(HmacHashFunction.valueOf("HmacSHA1"), config.getHmacHashFunction());
        assertEquals(7, config.getNumberOfScratchCodes());
        assertEquals(160, config.getSecretBits());
    }
}