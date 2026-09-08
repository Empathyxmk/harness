package com.example.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import org.joda.time.DateTime;
import org.joda.time.Duration;
import org.joda.time.DateTimeZone;
import org.joda.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

import com.example.delorean.dates;

public class TestDates {

    @Test
    public void testGetTotalSecondBasic() {
        Duration dur = new Duration(1 * 24 * 3600 * 1000 + 1000 + 0); // 1 day, 1 second
        double totalSec = dates.getTotalSecond(dur);
        // Tolerance check, assuming custom implementation similar to python
        assertTrue(Math.abs(totalSec - (1 * 24 * 3600 + 1)) < 1e-6);
    }

    @Test
    public void testIsDateTimeNaive() {
        LocalDateTime dt = new LocalDateTime();
        assertTrue(dates.isDateTimeNaive(dt));
        DateTime dtAware = dt.toDateTime(DateTimeZone.UTC);
        assertFalse(dates.isDateTimeNaive(dtAware));
    }

    @Test
    public void testIsDateTimeInstanceNone() {
        // None should simply return (no error)
        assertNull(dates.isDateTimeInstance(null));
    }

    @Test
    public void testIsDateTimeInstanceWrongType() {
        assertThrows(IllegalArgumentException.class, () -> {
            dates.isDateTimeInstance(123);
        });
    }

    @Test
    public void testMoveDateTimeDay() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = dates.moveDateTimeDay(dt, "next", 5);
        assertEquals(6, result.getDayOfMonth());
        DateTime result2 = dates.moveDateTimeDay(dt, "last", 1);
        assertTrue(result2.getDayOfMonth() == 31 || result2.getMonthOfYear() == 12);
    }

    @Test
    public void testMoveDateTimeHour() {
        DateTime dt = new DateTime(2020, 1, 1, 4, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = dates.moveDateTimeHour(dt, "next", 2);
        assertEquals(6, result.getHourOfDay());
        DateTime result2 = dates.moveDateTimeHour(dt, "last", 3);
        assertEquals(1, result2.getHourOfDay());
    }

    @Test
    public void testMoveDateTimeMinute() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = dates.moveDateTimeMinute(dt, "next", 45);
        assertEquals(45, result.getMinuteOfHour());
    }

    @Test
    public void testMoveDateTimeSecond() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 30, 0, DateTimeZone.UTC);
        DateTime result = dates.moveDateTimeSecond(dt, "next", 29);
        assertEquals(59, result.getSecondOfMinute());
    }

    @Test
    public void testMoveDateTimeMonth() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = dates.moveDateTimeMonth(dt, "next", 2);
        assertEquals(3, result.getMonthOfYear());
        DateTime result2 = dates.moveDateTimeMonth(dt, "last", 1);
        assertEquals(12, result2.getMonthOfYear());
        assertEquals(2019, result2.getYear());
    }

    @Test
    public void testMoveDateTimeWeek() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = dates.moveDateTimeWeek(dt, "next", 2);
        assertTrue(result.getDayOfMonth() == 8 || result.getDayOfMonth() == 15);
    }

    @Test
    public void testMoveDateTimeYear() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = dates.moveDateTimeYear(dt, "next", 2);
        assertEquals(2022, result.getYear());
        DateTime result2 = dates.moveDateTimeYear(dt, "last", 1);
        assertEquals(2019, result2.getYear());
    }

    @ParameterizedTest
    @CsvSource({
        // current, target, direction, expected_days
        "Monday,Tuesday,next,7",
        "Saturday,Monday,next,1",
        "Friday,Wednesday,last,-3",
        "Wednesday,Wednesday,next,6",
        "Sunday,Friday,last,-3"
    })
    public void testMoveDateTimeNamedDay(String current, String target, String direction, int expectedDays) {
        int[] dayMap = {6,7,8,9,10,11,12};
        String[] names = {"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"};
        int day = -1;
        for (int i=0; i<names.length; i++) {
            if (names[i].equals(current)) {
                day = dayMap[i];
            }
        }
        DateTime dt = new DateTime(2021, 4, day, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime moved = dates.moveDateTimeNamedDay(dt, direction, target);
        int diff = (int)((moved.getMillis() - dt.getMillis()) / (24*60*60*1000));
        assertEquals(expectedDays, diff);
    }

    @Test
    public void testDateTimeTimezoneAndLocalizeNormalize() {
        DateTime result = dates.datetimeTimezone("US/Pacific");
        assertNotNull(result.getZone());
        assertNotNull(result.getZone().getID());

        DateTime naiveDt = new DateTime(2023, 1, 1, 0, 0, 0, 0);
        DateTime aware = dates.localize(naiveDt, "UTC");
        assertNotNull(aware.getZone());

        DateTime aware2 = dates.localize(naiveDt, DateTimeZone.UTC);
        assertNotNull(aware2.getZone());
    }

    @Test
    public void testNormalizeValid() {
        DateTime d1 = new DateTime(2021, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime normalized = dates.normalize(d1, "US/Pacific");
        assertTrue(normalized.getZone().getID().contains("Pacific"));
    }

    @Test
    public void testNormalizeInvalidTimezone() {
        DateTime d1 = new DateTime(2021, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        assertThrows(Exception.class, () -> {
            dates.normalize(d1, "Invalid/Zone");
        });
    }
}