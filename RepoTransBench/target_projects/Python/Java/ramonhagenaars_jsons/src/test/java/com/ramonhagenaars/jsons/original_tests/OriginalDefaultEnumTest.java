package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultEnumTest {

    enum Day {
        MON, TUE, WED, THU, FRI, SAT, SUN
    }

    @Test
    void testEnumToString() {
        Day d = Day.FRI;
        assertEquals("FRI", d.toString());
    }

    @Test
    void testEnumValueOf() {
        Day d = Day.valueOf("TUE");
        assertEquals(Day.TUE, d);
    }
}