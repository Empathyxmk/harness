package com.ramonhagenaars.jsons.public_tests;

import org.junit.jupiter.api.Test;
import java.time.ZoneId;
import java.time.ZoneOffset;

import static org.junit.jupiter.api.Assertions.*;

public class PublicDefaultTimezoneTest {

    @Test
    void testDefaultTimezoneDumpPublic() {
        ZoneOffset offset = ZoneOffset.ofHours(2);
        assertEquals("+02:00", offset.toString());
    }

    @Test
    void testDefaultTimezoneLoadPublic() {
        ZoneId zone = ZoneId.of("UTC");
        assertEquals("UTC", zone.getId());
    }
}