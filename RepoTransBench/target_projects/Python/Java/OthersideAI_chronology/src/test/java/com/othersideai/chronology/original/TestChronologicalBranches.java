package com.othersideai.chronology.original;

import com.othersideai.chronology.Chronological;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestChronologicalBranches {
    @Test
    void testDummyPositive() {
        assertTrue(Chronological.dummyPositive(5));
        assertFalse(Chronological.dummyPositive(-3));
        assertFalse(Chronological.dummyPositive(0));
    }
}