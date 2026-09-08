package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestExceptionsHtmlCov {

    @Test
    public void testDeloreanErrorStr() {
        DeloreanError e = new DeloreanError("msg!");
        assertEquals("msg!", e.toString());
        assertTrue(e instanceof Exception);
    }

    @Test
    public void testDeloreanInvalidTimezoneIsSubclass() {
        DeloreanInvalidTimezone e = new DeloreanInvalidTimezone("bad tz");
        assertEquals("bad tz", e.toString());
        assertTrue(e instanceof DeloreanError);
    }

    @Test
    public void testDeloreanInvalidDatetimeIsSubclass() {
        DeloreanInvalidDatetime e = new DeloreanInvalidDatetime("bad dt");
        assertEquals("bad dt", e.toString());
        assertTrue(e instanceof DeloreanError);
    }
}

// You will need classes DeloreanError, DeloreanInvalidTimezone, DeloreanInvalidDatetime to exist in your delorean.exceptions package.