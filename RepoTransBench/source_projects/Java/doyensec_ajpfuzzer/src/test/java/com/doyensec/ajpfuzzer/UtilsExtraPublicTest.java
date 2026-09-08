package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class UtilsExtraPublicTest {

    @Test
    void testRandomStringAllCharsEdgeDifferent() {
        // Only one allowed char, different char
        String result = Utils.randomString(3, "z");
        assertEquals("zzz", result);
    }

    @Test
    void testGetRandomIntMinGreaterThanMaxThrowsDifferent() {
        assertThrows(IllegalArgumentException.class, () -> Utils.getRandomInt(10, 2));
    }

    @Test
    void testCreateMapFromPairsTypeSafetyDifferent() {
        Map<String, Double> m = Utils.createMapFromPairs("x", 0.1, "y", 2.2);
        assertEquals(0.1, m.get("x"));
        assertEquals(2.2, m.get("y"));
    }

    @Test
    void testToHexUpperByteValuesDifferent() {
        byte[] arr = { (byte)0xde, (byte)0xad, (byte)0xbe, (byte)0xef };
        String hex = Utils.toHex(arr);
        assertEquals("deadbeef", hex);
    }

    @Test
    void testJoinWithOnlyOneElementDifferent() {
        String[] arr = { "onlyone" };
        assertEquals("onlyone", Utils.join(arr, ","));
    }
}