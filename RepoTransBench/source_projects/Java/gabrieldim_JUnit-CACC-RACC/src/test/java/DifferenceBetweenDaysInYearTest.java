package gabrieldim_JUnitCACC;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DifferenceBetweenDaysInYearTest {

    @Test
    void testSameDay() {
        assertEquals(0, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 1, 1, 2023, 1, 1));
    }

    @Test
    void testNonLeapYearNormalDates() {
        // Jan 1 and Dec 31, 2023
        assertEquals(364, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 1, 1, 2023, 12, 31));
        assertEquals(-364, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 12, 31, 2023, 1, 1));
    }

    @Test
    void testLeapYearFebDates() {
        // Feb 28 & Feb 29 in leap year
        assertEquals(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2020, 2, 28, 2020, 2, 29));
        // Mar 1 & Feb 29
        assertEquals(-1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2020, 3, 1, 2020, 2, 29));
    }

    @Test
    void testInvalidMonth() {
        Exception e1 = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 0, 10, 2023, 1, 1)
        );
        String m = e1.getMessage();
        assertTrue(m != null && m.contains("Invalid"));
        Exception e2 = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 1, 1, 2023, 13, 1)
        );
        assertTrue(e2.getMessage().contains("Invalid"));
    }

    @Test
    void testInvalidDay() {
        // Feb 30 non-leap
        Exception e = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2021, 2, 30, 2021, 2, 1)
        );
        assertTrue(e.getMessage().contains("Invalid"));
        // Apr 31
        Exception e2 = assertThrows(IllegalArgumentException.class, () -> 
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 4, 31, 2022, 2, 1)
        );
        assertTrue(e2.getMessage().contains("Invalid"));
    }

    @Test
    void testDifferentYears() {
        Exception e = assertThrows(IllegalArgumentException.class, () ->
            DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 1, 1, 2021, 1, 1)
        );
        assertTrue(e.getMessage().contains("Years must be the same"));
    }

    @Test
    void testLeapYearRecognition() {
        // 2000 is a leap year, so Jan 1 -> Mar 1 is 60 days
        assertEquals(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2000, 1, 1, 2000, 3, 1)); // 2000 leap
        assertEquals(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2016, 1, 1, 2016, 3, 1)); // leap
        assertEquals(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2100, 1, 1, 2100, 3, 1)); // 2100 not leap
        assertEquals(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(1900, 1, 1, 1900, 3, 1)); // 1900 not leap
    }

    @Test
    void testFirstAndLastDaysOfMonth() {
        assertEquals(30, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 1, 2024, 1, 31));
        assertEquals(-30, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 31, 2024, 1, 1));
    }

    // Additional test for boundary values and uncovered paths
    @Test
    void testMinimumValidDayAndMonth() {
        // Jan 1, Jan 2
        assertEquals(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 1, 2024, 1, 2));
        // Jan 2, Jan 1 (negative)
        assertEquals(-1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 2, 2024, 1, 1));
    }

    @Test
    void testMaximumValidDayAndMonth() {
        // Dec 30, Dec 31
        assertEquals(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 12, 30, 2024, 12, 31));
    }

    @Test
    void testIsValidDatePrivateMethodViaInvalidInput() {
        // Covers daysInMonth array for February on leap and non-leap years
        Exception e1 = assertThrows(IllegalArgumentException.class, () ->
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2021, 2, 29, 2021, 2, 28));  // 2021 is not leap
        assertTrue(e1.getMessage().contains("Invalid"));

        Exception e2 = assertThrows(IllegalArgumentException.class, () ->
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2020, 2, 30, 2020, 2, 28));  // 2020 is leap, Feb has only 29
        assertTrue(e2.getMessage().contains("Invalid"));
    }
}