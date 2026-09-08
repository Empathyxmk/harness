package com.example.protontricks.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class WinetricksFuncTest {

    static int runFunc(int a, int b) {
        return a + b;
    }

    @Test
    void testWinetricksFunc() {
        assertEquals(5, runFunc(2, 3));
        assertEquals(7, runFunc(10, -3));
    }
}