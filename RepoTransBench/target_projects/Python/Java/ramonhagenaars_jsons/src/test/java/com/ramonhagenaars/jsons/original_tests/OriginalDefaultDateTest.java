package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import java.time.LocalDate;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultDateTest {

    @Test
    void testDateToString() {
        LocalDate date = LocalDate.of(2021, 4, 21);
        assertEquals("2021-04-21", date.toString());
    }

    @Test
    void testDateParse() {
        LocalDate date = LocalDate.parse("2019-07-19");
        assertEquals(2019, date.getYear());
        assertEquals(7, date.getMonthValue());
        assertEquals(19, date.getDayOfMonth());
    }
}