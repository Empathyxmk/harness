package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.time.Duration;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultTimedeltaTest {

    @Test
    void testDurationToSeconds() {
        Duration d = Duration.ofHours(2).plusMinutes(3).plusSeconds(30);
        assertEquals(2 * 3600 + 3 * 60 + 30, d.getSeconds());
    }

    @Test
    void testDurationFromSeconds() {
        Duration d = Duration.ofSeconds(86410);
        assertEquals(1, d.toDays());
        assertEquals(10, d.minusDays(1).getSeconds());
    }
}