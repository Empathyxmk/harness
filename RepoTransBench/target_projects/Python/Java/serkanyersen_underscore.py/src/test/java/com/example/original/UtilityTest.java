package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class UtilityTest {
    @Test
    void testRandom() {
        int num = Underscore.random(1, 10);
        assertTrue(num >= 1 && num <= 10);
    }
}