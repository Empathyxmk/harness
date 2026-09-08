package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.time.LocalDateTime;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultDatetimeTest {

    @Test
    void testDatetimeToString() {
        LocalDateTime dt = LocalDateTime.of(2023, 12, 25, 19, 30, 12, 999_000_000);
        assertTrue(dt.toString().startsWith("2023-12-25T19:30:12"));
    }

    @Test
    void testDatetimeParse() {
        LocalDateTime dt = LocalDateTime.parse("2018-02-03T10:11:12.123456789");
        assertEquals(2018, dt.getYear());
        assertEquals(2, dt.getMonthValue());
        assertEquals(3, dt.getDayOfMonth());
        assertEquals(10, dt.getHour());
        assertEquals(11, dt.getMinute());
        assertEquals(12, dt.getSecond());
        assertEquals(123456789, dt.getNano());
    }
}