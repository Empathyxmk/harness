package com.othersideai.chronology.public_tests;

import com.othersideai.chronology.Chronological;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicChronologicalBranchesTest {
    @Test
    void testDummyPositivePublic() {
        assertTrue(Chronological.dummyPositive(42));
        assertFalse(Chronological.dummyPositive(-17));
        assertFalse(Chronological.dummyPositive(0));
    }
}