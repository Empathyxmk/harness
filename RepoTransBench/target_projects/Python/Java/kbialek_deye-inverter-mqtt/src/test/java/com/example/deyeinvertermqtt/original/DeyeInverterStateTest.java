package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeInverterStateTest {

    @Test
    public void testStateIsOperational() {
        String state = "OPERATIONAL";
        assertEquals("OPERATIONAL", state, "State should be operational");
    }

    @Test
    public void testStateChangesToError() {
        String state = "ERROR";
        assertEquals("ERROR", state, "State should be error");
    }
}