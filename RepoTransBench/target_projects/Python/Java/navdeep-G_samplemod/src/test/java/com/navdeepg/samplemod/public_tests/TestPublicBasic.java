package com.navdeepg.samplemod.public_tests;

import com.navdeepg.samplemod.core.Core;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicBasic {

    @Test
    void testAddPositiveNumbersPublic() {
        assertEquals(15, Core.add(10, 5));
    }

    @Test
    void testAddNegativeAndPositivePublic() {
        assertEquals(-2, Core.add(-6, 4));
    }

    @Test
    void testAddZeroPublic() {
        assertEquals(19, Core.add(0, 19));
    }
}