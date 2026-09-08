package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicUtils {

    int clamp(int v, int min, int max) {
        if (v < min) return min;
        if (v > max) return max;
        return v;
    }

    @Test
    public void testClampPublic() {
        assertEquals(135, clamp(135, 100, 140));
        assertEquals(100, clamp(90, 100, 140));
        assertEquals(140, clamp(145, 100, 140));
    }
}