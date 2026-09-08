package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicPipeClassTest {
    static class Multiplier {
        int factor;
        Multiplier(int f) { factor = f; }
        int apply(int x) { return x * factor; }
    }

    @Test
    void testMultiplierPipeClass() {
        Multiplier times3 = new Multiplier(3);
        assertEquals(9, times3.apply(3));
        assertEquals(21, times3.apply(7));
    }

    @Test
    void testMultiplierPipeClassDifferentFactor() {
        Multiplier times10 = new Multiplier(10);
        assertEquals(100, times10.apply(10));
        assertEquals(50, times10.apply(5));
    }
}