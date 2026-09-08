package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicQuickTest {
    int square(int n) { return n * n; }
    int cube(int n) { return n * n * n; }

    @Test
    void testQuickSquare() {
        assertEquals(16, square(4));
        assertEquals(9, square(3));
        assertEquals(1, square(1));
    }

    @Test
    void testQuickCube() {
        assertEquals(8, cube(2));
        assertEquals(27, cube(3));
    }
}