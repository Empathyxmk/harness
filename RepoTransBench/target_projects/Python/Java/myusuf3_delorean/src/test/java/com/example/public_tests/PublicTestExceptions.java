package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.example.delorean.exceptions.DeloreanError;
import com.example.delorean.exceptions.DeloreanInvalidTimezone;
import com.example.delorean.exceptions.DeloreanInvalidDatetime;

public class PublicTestExceptions {

    @Test
    public void testDeloreanErrorStrPublic() {
        DeloreanError e = new DeloreanError("public error!");
        assertEquals("public error!", e.toString());
        assertTrue(e instanceof Exception);
    }

    @Test
    public void testDeloreanInvalidTimezoneIsSubclassPublic() {
        DeloreanInvalidTimezone e = new DeloreanInvalidTimezone("public bad tz");
        assertEquals("public bad tz", e.toString());
        assertTrue(e instanceof DeloreanError);
    }

    @Test
    public void testDeloreanInvalidDatetimeIsSubclassPublic() {
        DeloreanInvalidDatetime e = new DeloreanInvalidDatetime("public bad dt");
        assertEquals("public bad dt", e.toString());
        assertTrue(e instanceof DeloreanError);
    }
}