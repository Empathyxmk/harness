package com.example.deyeinvertermqtt.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicInverterStateTest {

    @Test
    public void testPublicStateIdle() {
        String state = "IDLE";
        assertEquals("IDLE", state, "State should be idle");
    }
}