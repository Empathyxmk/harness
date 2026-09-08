package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.time.LocalTime;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultTimeTest {

    @Test
    void testTimeOf() {
        LocalTime t = LocalTime.of(23, 58, 1);
        assertEquals(23, t.getHour());
        assertEquals(58, t.getMinute());
        assertEquals(1, t.getSecond());
    }

    @Test
    void testTimeParse() {
        LocalTime t = LocalTime.parse("16:20:22");
        assertEquals(16, t.getHour());
        assertEquals(20, t.getMinute());
        assertEquals(22, t.getSecond());
    }
}