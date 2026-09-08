package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PipeManualTest {

    private int addOne(int x) {
        return x + 1;
    }

    private int timesThree(int x) {
        return x * 3;
    }

    @Test
    void testManualPipeSequence() {
        int initial = 2;
        int afterFirst = addOne(initial);  // 3
        int finalResult = timesThree(afterFirst); // 9
        assertEquals(9, finalResult);
    }
}