package gabrieldim_JUnitCACC;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DifferenceBetweenDaysInYearPublicTest {

    @Test
    void publicTestSameDay() {
        assertEquals(0, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 5, 20, 2022, 5, 20));
    }

    @Test
    void publicTestNonLeapYearNormalDates() {
        // Mar 15 and Nov 27, 2022
        assertEquals(257, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 3, 15, 2022, 11, 27));
        assertEquals(-257, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 11, 27, 2022, 3, 15));
    }

    @Test
    void publicTestLeapYearFebDates() {
        // Feb 27 & Feb 28 in leap year
        assertEquals(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2016, 2, 27, 2016, 2, 28));
        // Mar 1 & Feb 28
        assertEquals(-2, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2016, 3, 1, 2016, 2, 28));
    }

    @Test
    void publicTestInvalidMonth() {
        Exception e1 = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 0, 4, 2022, 6, 9)
        );
        String m = e1.getMessage();
        assertTrue(m != null && m.contains("Invalid"));
        Exception e2 = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 3, 14, 2022, 15, 7)
        );
        assertTrue(e2.getMessage().contains("Invalid"));
    }

    @Test
    void publicTestInvalidDay() {
        // Feb 30 non-leap
        Exception e = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 30, 2023, 2, 1)
        );
        assertTrue(e.getMessage().contains("Invalid"));
        // Jun 31
        Exception e2 = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(1999, 6, 31, 1999, 3, 1)
        );
        assertTrue(e2.getMessage().contains("Invalid"));
    }

    @Test
    void publicTestDifferentYears() {
        Exception e = assertThrows(IllegalArgumentException.class, () ->
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2021, 4, 10, 2020, 5, 10)
        );
        assertTrue(e.getMessage().contains("Years must be the same"));
    }

    @Test
    void publicTestLeapYearRecognition() {
        // 2012 is a leap year, so Jan 1 -> Mar 1 is 60 days
        assertEquals(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2012, 1, 1, 2012, 3, 1)); // 2012 leap
        assertEquals(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2104, 1, 1, 2104, 3, 1)); // not leap
        assertEquals(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(1800, 1, 1, 1800, 3, 1)); // not leap
        assertEquals(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2400, 1, 1, 2400, 3, 1)); // leap
    }

    @Test
    void publicTestFirstAndLastDaysOfMonth() {
        assertEquals(27, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 4, 1, 2022, 4, 28));
        assertEquals(-27, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 4, 28, 2022, 4, 1));
    }

    @Test
    void publicTestMinimumValidDayAndMonth() {
        // Feb 1, Feb 2
        assertEquals(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 1, 2023, 2, 2));
        // Feb 2, Feb 1 (negative)
        assertEquals(-1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 2, 2023, 2, 1));
    }

    @Test
    void publicTestMaximumValidDayAndMonth() {
        // Nov 29, Nov 30
        assertEquals(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 11, 29, 2023, 11, 30));
    }

    @Test
    void publicTestIsValidDatePrivateMethodViaInvalidInput() {
        // Feb 29 on non-leap year
        Exception e1 = assertThrows(IllegalArgumentException.class, () ->
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 29, 2023, 2, 28));
        assertTrue(e1.getMessage().contains("Invalid"));

        // Feb 30 on leap year (29 only)
        Exception e2 = assertThrows(IllegalArgumentException.class, () ->
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 2, 30, 2024, 2, 28));
        assertTrue(e2.getMessage().contains("Invalid"));
    }
}