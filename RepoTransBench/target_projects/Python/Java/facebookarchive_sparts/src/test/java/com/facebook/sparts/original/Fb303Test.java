package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Fb303Test {
    @Test
    public void testSimpleMath() {
        assertEquals(45, 5 * 9);
        assertTrue(18 > 9);
        assertFalse(7 > 88);
    }
}