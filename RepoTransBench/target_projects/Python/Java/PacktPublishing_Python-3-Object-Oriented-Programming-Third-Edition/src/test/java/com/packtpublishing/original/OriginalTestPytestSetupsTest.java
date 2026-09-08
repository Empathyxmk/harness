package com.packtpublishing.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class OriginalTestPytestSetupsTest {

    int counter;

    @BeforeEach
    void setupCounter() {
        counter = 5;
    }

    @Test
    void testCounterIsFive() {
        assertEquals(5, counter);
    }

    @Test
    void testAddToCounter() {
        counter += 2;
        assertEquals(7, counter);
    }

    @AfterEach
    void teardownCounter() {
        counter = 0;
    }
}