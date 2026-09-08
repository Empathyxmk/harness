package com.seatgeek.public_tests;

import com.seatgeek.fuzzywuzzy.Process;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PublicProcessPyTest {
    @Test
    void testExtractOnePublic() {
        String query = "python programmer";
        List<String> choices = Arrays.asList("java developer", "python engineer", "c++ guru");
        Object[] res = Process.extractOne(query, choices);
        String match = (String) res[0];
        int score = (int) res[1];
        assertTrue(choices.contains(match));
        assertTrue(score > 0);
    }

    @Test
    void testExtractBestsPublic() {
        String query = "data science";
        List<String> choices = Arrays.asList("science data", "data analytics", "data scientist", "big data");
        List<Object[]> results = Process.extractBests(query, choices, 2);
        assertEquals(2, results.size());
        for (Object[] pair : results) {
            String match = (String) pair[0];
            int score = (int) pair[1];
            assertTrue(choices.contains(match));
            assertTrue(score > 0);
        }
    }
}