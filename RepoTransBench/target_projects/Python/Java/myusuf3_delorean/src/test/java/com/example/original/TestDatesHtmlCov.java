package com.example.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.Arguments;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.Duration;

import static org.junit.jupiter.api.Assertions.*;

import java.util.stream.Stream;

public class TestDatesHtmlCov {

    @Test
    public void testGetTotalSecondBasic() {
        // timedelta(days=1, seconds=1, microseconds=1)
        Duration td = new Duration((1 * 24 * 3600 + 1) * 1000 + 0); // microseconds is negligible in Duration
        double micro = 1e-6;
        double total = DatesUtil.getTotalSecond(td) + micro;
        assertTrue(Math.abs(total - (1 * 24 * 3600 + 1 + micro)) < 1e-6);
    }

    @Test
    public void testIsDateTimeNaive() {
        DateTime dt = DateTime.now();
        assertTrue(DatesUtil.isDateTimeNaive(dt));
        DateTime dtAware = dt.withZone(DateTimeZone.UTC);
        assertFalse(DatesUtil.isDateTimeNaive(dtAware));
    }

    @Test
    public void testIsDateTimeInstanceNone() {
        assertNull(DatesUtil.isDateTimeInstance(null));
    }

    @Test
    public void testIsDateTimeInstanceWrongType() {
        assertThrows(IllegalArgumentException.class, () -> DatesUtil.isDateTimeInstance(123));
    }

    @Test
    public void testMoveDateTimeDay() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = DatesUtil.moveDateTimeDay(dt, "next", 5);
        assertEquals(6, result.getDayOfMonth());
        DateTime result2 = DatesUtil.moveDateTimeDay(dt, "last", 1);
        assertTrue(result2.getDayOfMonth() == 31 || result2.getMonthOfYear() == 12);
    }

    @Test
    public void testMoveDateTimeHour() {
        DateTime dt = new DateTime(2020, 1, 1, 4, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = DatesUtil.moveDateTimeHour(dt, "next", 2);
        assertEquals(6, result.getHourOfDay());
        DateTime result2 = DatesUtil.moveDateTimeHour(dt, "last", 3);
        assertEquals(1, result2.getHourOfDay());
    }

    @Test
    public void testMoveDateTimeMinute() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = DatesUtil.moveDateTimeMinute(dt, "next", 45);
        assertEquals(45, result.getMinuteOfHour());
    }

    @Test
    public void testMoveDateTimeSecond() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 30, 0, DateTimeZone.UTC);
        DateTime result = DatesUtil.moveDateTimeSecond(dt, "next", 29);
        assertEquals(59, result.getSecondOfMinute());
    }

    @Test
    public void testMoveDateTimeMonth() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = DatesUtil.moveDateTimeMonth(dt, "next", 2);
        assertEquals(3, result.getMonthOfYear());
        DateTime result2 = DatesUtil.moveDateTimeMonth(dt, "last", 1);
        assertTrue(result2.getMonthOfYear() == 12 && result2.getYear() == 2019);
    }

    @Test
    public void testMoveDateTimeWeek() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = DatesUtil.moveDateTimeWeek(dt, "next", 2);
        assertTrue(result.getDayOfMonth() == 8 || result.getDayOfMonth() == 15);
    }

    @Test
    public void testMoveDateTimeYear() {
        DateTime dt = new DateTime(2020, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime result = DatesUtil.moveDateTimeYear(dt, "next", 2);
        assertEquals(2022, result.getYear());
        DateTime result2 = DatesUtil.moveDateTimeYear(dt, "last", 1);
        assertEquals(2019, result2.getYear());
    }

    public static Stream<Arguments> moveNamedDayProvider() {
        return Stream.of(
            Arguments.of("Monday", "Tuesday", "next", 7),
            Arguments.of("Saturday", "Monday", "next", 1),
            Arguments.of("Friday", "Wednesday", "last", -3),
            Arguments.of("Wednesday", "Wednesday", "next", 6),
            Arguments.of("Sunday", "Friday", "last", -3)
        );
    }

    @ParameterizedTest
    @MethodSource("moveNamedDayProvider")
    public void testMoveDateTimeNamedDay(String current, String target, String direction, int expectedDays) {
        java.util.Map<String, Integer> days = new java.util.HashMap<>();
        days.put("Monday", 6);
        days.put("Tuesday", 7);
        days.put("Wednesday", 8);
        days.put("Thursday", 9);
        days.put("Friday", 10);
        days.put("Saturday", 11);
        days.put("Sunday", 12);

        int dayNum = days.get(current);
        DateTime dt = new DateTime(2021, 4, dayNum, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime moved = DatesUtil.moveDateTimeNamedDay(dt, direction, target);
        long diff = (moved.getMillis() - dt.getMillis()) / (24*60*60*1000);
        assertEquals(expectedDays, diff);
    }

    @Test
    public void testDateTimeTimezoneAndLocalizeNormalize() {
        DateTime result = DatesUtil.datetimeTimezone("US/Pacific");
        assertNotNull(result.getZone());

        DateTime naiveDt = new DateTime(2023, 1, 1, 0, 0, 0, 0);
        DateTime aware = DatesUtil.localize(naiveDt, "UTC");
        assertNotNull(aware.getZone());

        DateTime aware2 = DatesUtil.localize(naiveDt, DateTimeZone.UTC);
        assertNotNull(aware2.getZone());
    }

    @Test
    public void testNormalizeValid() {
        DateTime d1 = new DateTime(2021, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        DateTime normalized = DatesUtil.normalize(d1, "US/Pacific");
        assertTrue(normalized.getZone().getID().contains("Pacific"));
    }

    @Test
    public void testNormalizeInvalidTimezone() {
        DateTime d1 = new DateTime(2021, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        assertThrows(Exception.class, () -> DatesUtil.normalize(d1, "Invalid/Zone"));
    }
}

// You will need to fully implement DatesUtil as a static helper class with all these methods.