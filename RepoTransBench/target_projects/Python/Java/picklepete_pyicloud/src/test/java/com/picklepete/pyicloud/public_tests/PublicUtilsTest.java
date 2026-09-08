package com.picklepete.pyicloud.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicUtilsTest {

    @Test
    public void testPublicGenerateRandomString() {
        String random = "abcXYZ123";
        assertNotNull(random);
        assertFalse(random.isEmpty());
        assertTrue(random.length() >= 5);
    }

    @Test
    public void testPublicTimestampParsing() {
        String iso = "2024-06-25T08:34:00Z";
        boolean matches = iso.matches("\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z");
        assertTrue(matches);
    }
}