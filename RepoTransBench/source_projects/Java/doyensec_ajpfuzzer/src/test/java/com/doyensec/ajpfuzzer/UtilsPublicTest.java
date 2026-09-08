package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class UtilsPublicTest {

    @Test
    void testRandomStringNegativeLengthDifferent() {
        assertThrows(IllegalArgumentException.class, () -> Utils.randomString(-5, "xyz"));
    }

    @Test
    void testRandomStringWithEmptyCharsDifferent() {
        assertThrows(IllegalArgumentException.class, () -> Utils.randomString(3, ""));
    }

    @Test
    void testRandomStringWithValidDifferentInput() {
        String result = Utils.randomString(6, "wxyz");
        assertNotNull(result);
        assertEquals(6, result.length());
        assertTrue(result.matches("[wxyz]{6}"));
    }

    @Test
    void testGetRandomIntEdgeCasesDifferent() {
        // min == max
        assertEquals(7, Utils.getRandomInt(7, 7));
        assertEquals(100, Utils.getRandomInt(100, 100));
    }

    @Test
    void testGetRandomIntRangeDifferent() {
        for (int i = 0; i < 50; ++i) {
            int result = Utils.getRandomInt(20, 30);
            assertTrue(result >= 20 && result <= 30);
        }
    }

    @Test
    void testCreateMapFromPairsEvenArgumentsDifferent() {
        Map<String, Object> map = Utils.createMapFromPairs("key1", 555, "key2", 789, "key3", "value3");
        assertEquals(3, map.size());
        assertEquals(555, map.get("key1"));
        assertEquals(789, map.get("key2"));
        assertEquals("value3", map.get("key3"));
    }

    @Test
    void testCreateMapFromPairsOddArgumentsDifferent() {
        assertThrows(IllegalArgumentException.class, () -> Utils.createMapFromPairs("foo", "bar", "baz"));
    }

    @Test
    void testToHexDifferent() {
        byte[] b = new byte[] {1, 11, 17, 22, 51, (byte)128, (byte)200};
        String hex = Utils.toHex(b);
        assertTrue(hex.matches("[0-9a-f]{14}"));
        assertEquals("010b11163380c8", hex);
    }

    @Test
    void testToHexNullDifferent() {
        assertNull(Utils.toHex(null));
    }

    @Test
    void testToHexEmptyDifferent() {
        assertEquals("", Utils.toHex(new byte[0]));
    }

    @Test
    void testJoinSimpleDifferent() {
        String[] arr = new String[] {"foo", "bar", "baz"};
        String result = Utils.join(arr, "-");
        assertEquals("foo-bar-baz", result);
    }

    @Test
    void testJoinNullDifferent() {
        assertEquals("", Utils.join(null, "&"));
    }

    @Test
    void testJoinEmptyArrayDifferent() {
        assertEquals("", Utils.join(new String[0], "~"));
    }

    @Test
    void testJoinNoSeparatorDifferent() {
        String[] arr = {"d","e","f"};
        assertEquals("def", Utils.join(arr, ""));
    }
}