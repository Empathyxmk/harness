package com.viralogic.enumerable.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestFixtures {

    private int shared;

    @BeforeEach
    void setup() {
        shared = 42;
    }

    @Test
    void testFixtureWorks() {
        assertEquals(42, shared);
    }

    @Test
    void testFixtureMutability() {
        shared += 1;
        assertEquals(43, shared);
    }
}