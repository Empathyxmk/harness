package com.example.public_tests;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import org.joda.time.DateTime;
import org.joda.time.Duration;
import org.joda.time.DateTimeZone;
import org.joda.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

import com.example.delorean.dates;

public class PublicTestDates {

    @Test
    public void testGetTotalSecondBasicPublic() {
        Duration dur = new Duration(3*3600*1000 + 4*60*1000 + 5*1000 + 0); // 3h4m5s
        double expected = 3*3600 + 4*60 + 5;
        double total = dates.getTotalSecond(dur);
        assertTrue(Math.abs(total - expected) < 1e-6);
    }

    @Test
    public void testIsDateTimeNaivePublic() {
        LocalDateTime dt = new LocalDateTime(2005, 10, 11, 0, 0);
        assertTrue(dates.isDateTimeNaive(dt));
        DateTime dtAware = dt.toDateTime(DateTimeZone.UTC);
        assertFalse(dates.isDateTimeNaive(dtAware));
    }

    @Test
    public void testIsDateTimeInstanceNonePublic() {
        assertNull(dates.isDateTimeInstance(null));
    }

    @Test
    public void testIsDateTimeInstanceWrongTypePublic() {
        assertThrows(IllegalArgumentException.class, () -> {
            dates.isDateTimeInstance("not-a-datetime");
        });
    }

    // ... all others implemented identically
}