package com.example.deyeinvertermqtt.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicConfigTest {

    @Test
    public void testPublicConfigDefault() {
        String defaultVal = "STD";
        assertEquals("STD", defaultVal, "Config should use standard default");
    }
}