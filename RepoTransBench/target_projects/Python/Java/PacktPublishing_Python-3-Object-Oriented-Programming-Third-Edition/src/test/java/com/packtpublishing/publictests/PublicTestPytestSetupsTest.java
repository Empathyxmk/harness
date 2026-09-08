package com.packtpublishing.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestPytestSetupsTest {
    int value;

    @BeforeEach
    void setup() {
        value = 2;
    }

    @Test
    void testValueIs2() {
        assertEquals(2, value);
    }

    @Test
    void testAdd() {
        value += 3;
        assertEquals(5, value);
    }
}