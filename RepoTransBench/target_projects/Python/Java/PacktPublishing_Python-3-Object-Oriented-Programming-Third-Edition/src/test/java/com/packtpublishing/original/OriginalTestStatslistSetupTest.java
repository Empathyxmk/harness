package com.packtpublishing.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class OriginalTestStatslistSetupTest {

    int[] values;

    @BeforeEach
    void setup() {
        values = new int[]{1,2,3,4,5};
    }

    @Test
    void testSum() {
        int sum = 0;
        for(int v: values) sum += v;
        assertEquals(15, sum);
    }

    @Test
    void testAverage() {
        int sum = 0;
        for(int v: values) sum += v;
        assertEquals(3.0, (double)sum/values.length);
    }

    @AfterEach
    void teardown() {
        // Cleanup code if needed
        values = null;
    }
}