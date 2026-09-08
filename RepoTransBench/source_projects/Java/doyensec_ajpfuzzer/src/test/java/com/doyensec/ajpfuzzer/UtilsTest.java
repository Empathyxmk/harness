package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;
import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {

    @Test
    void testRandomStringNegativeLength() {
        assertThrows(IllegalArgumentException.class, () -> Utils.randomString(-1, "abc"));
    }

    @Test
    void testRandomStringWithEmptyChars() {
        assertThrows(IllegalArgumentException.class, () -> Utils.randomString(5, ""));
    }

    @Test
    void testRandomStringWithValidInput() {
        String result = Utils.randomString(8, "abcd");
        assertNotNull(result);
        assertEquals(8, result.length());
        assertTrue(result.matches("[abcd]{8}"));
    }

    @Test
    void testGetRandomIntEdgeCases() {
        // min == max
        assertEquals(5, Utils.getRandomInt(5, 5));
        assertEquals(42, Utils.getRandomInt(42, 42));
    }

    @Test
    void testGetRandomIntRange() {
        for (int i = 0; i < 100; ++i) {
            int result = Utils.getRandomInt(10, 20);
            assertTrue(result >= 10 && result <= 20);
        }
    }

    @Test
    void testCreateMapFromPairsEvenArguments() {
        Map<String, Object> map = Utils.createMapFromPairs("k1", 123, "k2", "vv", "k3", null);
        assertEquals(3, map.size());
        assertEquals(123, map.get("k1"));
        assertEquals("vv", map.get("k2"));
        assertNull(map.get("k3"));
    }

    @Test
    void testCreateMapFromPairsOddArguments() {
        assertThrows(IllegalArgumentException.class, () -> Utils.createMapFromPairs("a", "b", "c"));
    }

    @Test
    void testToHex() {
        byte[] b = new byte[] {0, 10, 15, 16, 31, 127, (byte)255};
        String hex = Utils.toHex(b);
        assertTrue(hex.matches("[0-9a-f]{14}"));
        assertEquals("000a0f101f7fff", hex);
    }

    @Test
    void testToHexNull() {
        assertNull(Utils.toHex(null));
    }

    @Test
    void testToHexEmpty() {
        assertEquals("", Utils.toHex(new byte[0]));
    }

    @Test
    void testJoinSimple() {
        String[] arr = new String[] {"a", "b", "c"};
        String result = Utils.join(arr, ":");
        assertEquals("a:b:c", result);
    }

    @Test
    void testJoinNull() {
        assertEquals("", Utils.join(null, ","));
    }

    @Test
    void testJoinEmptyArray() {
        assertEquals("", Utils.join(new String[0], "|"));
    }

    @Test
    void testJoinNoSeparator() {
        String[] arr = {"x","y"};
        assertEquals("xy", Utils.join(arr, ""));
    }
}