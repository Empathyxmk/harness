package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Utils {
    public static int max(int a, int b) { return a > b ? a : b; }
    public static boolean isEven(int n) { return n % 2 == 0; }
}

public class PublicUtilsTest {
    @Test
    void testMaxUtil() {
        assertEquals(9, Utils.max(4,9));
        assertEquals(-1, Utils.max(-1, -3));
    }

    @Test
    void testIsEvenUtil() {
        assertTrue(Utils.isEven(10));
        assertFalse(Utils.isEven(7));
    }
}