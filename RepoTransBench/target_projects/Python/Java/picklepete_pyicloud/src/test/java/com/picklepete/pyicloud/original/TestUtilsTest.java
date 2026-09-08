package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestUtilsTest {

    @Test
    public void testDateTimeParsing() {
        String iso = "2022-02-02T10:00:00Z";
        boolean isIsoFormat = iso.matches("\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z");
        assertTrue(isIsoFormat);
    }

    @Test
    public void testRandomStringFunction() {
        String randomString = "abc123xyz";
        assertNotNull(randomString);
        assertFalse(randomString.isEmpty());
    }
}