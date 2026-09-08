package com.othersideai.chronology.original;

import com.othersideai.chronology.Chronological;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class TestChronologicalExtra {
    @Test
    void testDummyMul() {
        assertEquals(6, Chronological.dummyMul(2, 3));
        assertEquals(-1, Chronological.dummyMul(-1, 1));
        assertEquals(0, Chronological.dummyMul(0, 5));
    }
}