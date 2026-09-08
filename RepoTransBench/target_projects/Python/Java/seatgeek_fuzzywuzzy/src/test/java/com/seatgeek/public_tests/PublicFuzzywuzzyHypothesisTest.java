package com.seatgeek.public_tests;

import com.seatgeek.fuzzywuzzy.Fuzz;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicFuzzywuzzyHypothesisTest {

    @Test
    void testPublicTokenSortRatioSymmetry() {
        String s1 = "San Francisco Giants";
        String s2 = "giants san francisco";
        int r1 = Fuzz.tokenSortRatio(s1, s2);
        int r2 = Fuzz.tokenSortRatio(s2, s1);
        assertEquals(r1, r2);
        assertEquals(100, r1);
    }

    @Test
    void testPublicTokenSetRatioSymmetry() {
        String s1 = "new york giants";
        String s2 = "giants new york";
        int r1 = Fuzz.tokenSetRatio(s1, s2);
        int r2 = Fuzz.tokenSetRatio(s2, s1);
        assertEquals(r1, r2);
        assertEquals(100, r1);
    }
}