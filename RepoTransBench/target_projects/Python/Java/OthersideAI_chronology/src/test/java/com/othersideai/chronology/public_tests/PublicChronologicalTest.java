package com.othersideai.chronology.public_tests;

import com.othersideai.chronology.Chronological;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicChronologicalTest {
    @Test
    void testDummyAddPublic() {
        assertEquals(12, Chronological.dummyAdd(8, 4));
        assertEquals(5, Chronological.dummyAdd(-5, 10));
        assertEquals(0, Chronological.dummyAdd(7, -7));
    }
}