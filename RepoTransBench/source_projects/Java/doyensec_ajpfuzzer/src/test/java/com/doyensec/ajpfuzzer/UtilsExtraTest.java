package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class UtilsExtraTest {

    @Test
    void testRandomStringAllCharsEdge() {
        // Only one allowed char, should repeat
        String result = Utils.randomString(5, "x");
        assertEquals("xxxxx", result);
    }

    @Test
    void testGetRandomIntMinGreaterThanMaxThrows() {
        assertThrows(IllegalArgumentException.class, () -> Utils.getRandomInt(5, 2));
    }

    @Test
    void testCreateMapFromPairsTypeSafety() {
        Map<Integer, String> m = Utils.createMapFromPairs(1, "a", 2, "b");
        assertEquals("a", m.get(1));
        assertEquals("b", m.get(2));
    }

    @Test
    void testToHexUpperByteValues() {
        byte[] arr = { (byte)0xaf, (byte)0xff, (byte)0xb4 };
        String hex = Utils.toHex(arr);
        assertEquals("afffb4", hex);
    }

    @Test
    void testJoinWithOnlyOneElement() {
        String[] arr = { "solo" };
        assertEquals("solo", Utils.join(arr, ","));
    }
}