package com.othersideai.chronology.public_tests;

import com.othersideai.chronology.Chronological;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicChronologicalExtraTest {
    @Test
    void testDummyMulPublic() {
        assertEquals(20, Chronological.dummyMul(4, 5));
        assertEquals(-12, Chronological.dummyMul(-2, 6));
        assertEquals(0, Chronological.dummyMul(0, -3));
    }
}