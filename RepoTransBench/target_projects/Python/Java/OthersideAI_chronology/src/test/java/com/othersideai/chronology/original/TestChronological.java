package com.othersideai.chronology.original;

import com.othersideai.chronology.Chronological;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestChronological {
    @Test
    void testDummyAdd() {
        assertEquals(5, Chronological.dummyAdd(2, 3));
        assertEquals(0, Chronological.dummyAdd(-1, 1));
        assertEquals(0, Chronological.dummyAdd(0, 0));
    }
}