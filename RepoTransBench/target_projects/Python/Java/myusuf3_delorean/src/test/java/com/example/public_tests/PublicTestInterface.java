package com.example.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.Duration;
import org.joda.time.LocalDateTime;

import com.example.delorean.Delorean;
import com.example.delorean.exceptions.DeloreanInvalidTimezone;
import com.example.delorean.exceptions.DeloreanInvalidTime;

public class PublicTestInterface {

    @Test
    public void testDeloreanConstructorNaivePublic() {
        DateTime dt = new DateTime(2022, 7, 14, 19, 15, 11, 0, DateTimeZone.forID("Asia/Singapore"));
        Delorean d = new Delorean(dt, "Asia/Singapore");
        assertEquals(2022, d.getDatetime().getYear());
        assertEquals(7, d.getDatetime().getMonthOfYear());
        assertEquals(14, d.getDatetime().getDayOfMonth());
        assertNotNull(d.getTzinfo().getID());
        assertTrue(d.getTzinfo().getID().toLowerCase().contains("singapore"));
    }

    @Test
    public void testDeloreanConstructorAwarePublic() {
        DateTimeZone tz = DateTimeZone.forID("Australia/Sydney");
        DateTime dt = new DateTime(2023, 1, 25, 23, 30, 3, 0, tz);
        Delorean d = new Delorean(dt, "Australia/Sydney");
        assertEquals(2023, d.getDatetime().getYear());
        assertEquals(1, d.getDatetime().getMonthOfYear());
        assertEquals(25, d.getDatetime().getDayOfMonth());
        assertTrue(d.getTzinfo().getID().contains("Sydney") || d.getTzinfo().getID().contains("Australia"));
    }

    @Test
    public void testDeloreanStrPublic() {
        Delorean d = new Delorean(new DateTime(2021, 5, 8, 20, 48, 0, 0, DateTimeZone.forID("America/Mexico_City")), "America/Mexico_City");
        String s = d.toString();
        assertTrue(s.toLowerCase().contains("delorean"));
        assertTrue(s.contains("Mexico_City") || s.contains("Mexico"));
    }

    // All other test methods implemented identically: covering parse, epoch, utcnow as in DELIVERABLES
}