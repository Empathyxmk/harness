package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.time.ZoneId;
import java.time.ZoneOffset;

import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultTimezoneTest {

    @Test
    void testZoneId() {
        ZoneId utc = ZoneId.of("UTC");
        assertEquals("UTC", utc.getId());
        ZoneId paris = ZoneId.of("Europe/Paris");
        assertEquals("Europe/Paris", paris.getId());
    }

    @Test
    void testZoneOffset() {
        ZoneOffset offset = ZoneOffset.ofHours(-3);
        assertEquals("-03:00", offset.toString());
    }
}