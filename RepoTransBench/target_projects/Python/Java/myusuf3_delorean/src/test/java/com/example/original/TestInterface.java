package com.example.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;
import org.junit.jupiter.api.BeforeEach;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.MutableDateTime;
import org.joda.time.Period;
import org.joda.time.Duration;

import static org.junit.jupiter.api.Assertions.*;

import com.example.delorean.Delorean;
import com.example.delorean.exceptions.DeloreanInvalidTimezone;

public class TestInterface {

    @Test
    public void testDeloreanConstructorNaive() {
        DateTime dt = new DateTime(2022, 1, 2, 12, 0, 0, 0, DateTimeZone.UTC);
        Delorean d = new Delorean(dt.withZone(DateTimeZone.UTC), "UTC");
        assertEquals(dt, d.getDatetime());
        assertEquals("UTC", d.getTz().getID());
    }

    @Test
    public void testDeloreanConstructorTimezoneStrAndObj() {
        DateTime dt = new DateTime(2022, 1, 2, 13, 0, 0, 0, DateTimeZone.UTC);
        Delorean d1 = new Delorean(dt, "US/Pacific");
        assertEquals("US/Pacific", d1.getTz().getID());

        Delorean d2 = new Delorean(dt, DateTimeZone.forID("US/Eastern"));
        assertEquals("US/Eastern", d2.getTz().getID());
    }

    @Test
    public void testDeloreanConstructorInvalidTimezone() {
        DateTime dt = new DateTime(2022, 1, 2, 13, 0, 0, 0, DateTimeZone.UTC);
        assertThrows(DeloreanInvalidTimezone.class, () -> {
            new Delorean(dt, "Invalid/Zone");
        });
    }

    @Test
    public void testDeloreanShiftMinutesAndSeconds() {
        DateTime dt = new DateTime(2017, 5, 6, 12, 30, 0, 0, DateTimeZone.UTC);
        Delorean d = new Delorean(dt, "UTC");
        Delorean d2 = d.shift(2, 5, 0); // assuming shift(minutes, seconds, hours)
        assertEquals(32, d2.getDatetime().getMinuteOfHour());
        assertEquals(5, d2.getDatetime().getSecondOfMinute());
    }

    @Test
    public void testDeloreanNextLastMethods() {
        DateTime dt = new DateTime(2021, 12, 31, 23, 0, 0, 0, DateTimeZone.UTC);
        Delorean d = new Delorean(dt, "UTC");

        Delorean nextDay = d.nextDay();
        assertTrue(nextDay.getDatetime().getDayOfMonth() == 1 ||
                   nextDay.getDatetime().getMonthOfYear() == 1);

        Delorean lastWeek = d.lastWeek();
        int diffDays = Math.abs(d.getDatetime().getDayOfYear() - lastWeek.getDatetime().getDayOfYear());
        assertTrue(diffDays <= 7);
    }

    @Test
    public void testDeloreanTruncateToDay() {
        DateTime dt = new DateTime(2022, 3, 4, 15, 34, 56, 0, DateTimeZone.UTC);
        Delorean d = new Delorean(dt, "UTC");
        Delorean truncated = d.truncate("day");
        assertEquals(0, truncated.getDatetime().getHourOfDay());
        assertEquals(0, truncated.getDatetime().getMinuteOfHour());
    }

    @Test
    public void testDeloreanEqAndRepr() {
        DateTime dt = new DateTime(2022, 3, 4, 0, 0, 0, 0, DateTimeZone.UTC);
        Delorean d1 = new Delorean(dt, "UTC");
        Delorean d2 = new Delorean(dt, "UTC");
        assertEquals(d1, d2);
        assertTrue(d1.toString().contains("Delorean"));
    }

    @Test
    public void testDeloreanRollforwardRollbackup() {
        DateTime dt = new DateTime(2022, 3, 6, 0, 0, 0, 0, DateTimeZone.UTC);
        Delorean d = new Delorean(dt, "UTC");
        Delorean rf = d.rollforward("Monday");
        Delorean rb = d.rollback("Monday");
        assertNotNull(rf.getDatetime());
        assertNotNull(rb.getDatetime());
        // could land on the same if already Monday
        assertTrue(!rf.equals(d) || !rb.equals(d));
    }

    @Test
    public void testDeloreanTimezoneAndConvert() {
        DateTime dt = new DateTime(2021, 3, 1, 10, 0, 0, 0, DateTimeZone.UTC);
        Delorean d = new Delorean(dt, "UTC");
        Delorean local = d.localize("US/Pacific");
        assertEquals("US/Pacific", local.getTz().getID());
        Delorean norm = d.normalize("US/Pacific");
        assertEquals("US/Pacific", norm.getTz().getID());
        // toUnix, toJoda, toDateTime
        assertTrue(d.toUnix() instanceof Double);
        assertNotNull(d.toJoda().getZone());
        assertNotNull(d.toDateTime().getZone());
    }

    @Test
    public void testDeloreanConvertUnsupported() {
        DateTime dt = new DateTime(2022, 1, 1, 0, 0, 0, 0, DateTimeZone.UTC);
        Delorean d = new Delorean(dt, "UTC");
        assertThrows(IllegalArgumentException.class, () -> d.truncate("unknown"));
    }

    @Test
    public void testDeloreanFactoryMethods() {
        Delorean d1 = Delorean.utcnow();
        Delorean d2 = Delorean.now("UTC");
        Delorean d3 = Delorean.parse("2021-01-01T10:00:00Z");
        Delorean d4 = Delorean.epoch(0, "UTC");
        assertTrue(d1 instanceof Delorean);
        assertTrue(d2 instanceof Delorean);
        assertTrue(d3 instanceof Delorean);
        assertTrue(d4 instanceof Delorean);
        assertEquals(1970, d4.getDatetime().getYear());
    }
}