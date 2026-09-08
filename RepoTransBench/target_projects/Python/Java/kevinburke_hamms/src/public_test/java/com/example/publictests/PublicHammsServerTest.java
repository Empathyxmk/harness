package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

public class PublicHammsServerTest {

    @Test
    public void testPublicServerTrue() {
        assertEquals(20, 100 / 5);
    }

    @Test
    public void testPublicServerOther() {
        Map<String, Integer> config = new HashMap<>();
        config.put("foo", 5);
        config.put("bar", 9);
        assertTrue(config.containsKey("bar"));
    }
}