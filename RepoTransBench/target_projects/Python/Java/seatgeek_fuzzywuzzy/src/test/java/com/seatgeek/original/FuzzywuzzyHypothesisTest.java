package com.seatgeek.original;

import com.seatgeek.fuzzywuzzy.Fuzz;
import org.junit.jupiter.api.RepeatedTest;
import static org.junit.jupiter.api.Assertions.*;

class FuzzywuzzyHypothesisTest {

    @RepeatedTest(20)
    void testTokenSortUpperLowerSymmetry() {
        // Test tokenSortRatio is identical no matter the case
        StringBuilder builder = new StringBuilder();
        StringBuilder upperBuilder = new StringBuilder();
        for(int i=0;i<10;++i){
            String word = "abc" + i;
            builder.append(word);
            if (i != 9) builder.append(" ");
            upperBuilder.append(word.toUpperCase());
            if (i != 9) upperBuilder.append(" ");
        }
        String sample = builder.toString();
        String upper = upperBuilder.toString();
        int ratioLower = Fuzz.tokenSortRatio(sample, sample);
        int ratioUpper = Fuzz.tokenSortRatio(upper, upper);
        int ratioMixed = Fuzz.tokenSortRatio(upper, sample);
        assertEquals(ratioLower, 100);
        assertEquals(ratioUpper, 100);
        assertEquals(ratioMixed, 100);
    }

    @RepeatedTest(20)
    void testTokenSetSymmetry() {
        // Token set ratio (case-insensitive): identical strings == 100
        String sample = "foo bar baz qux";
        String rev = "qux baz bar foo";
        int ratio = Fuzz.tokenSetRatio(sample, rev);
        assertEquals(ratio, 100);
    }
}