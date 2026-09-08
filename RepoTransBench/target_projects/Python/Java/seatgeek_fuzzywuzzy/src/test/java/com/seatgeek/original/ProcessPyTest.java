package com.seatgeek.original;

import com.seatgeek.fuzzywuzzy.Process;
import com.seatgeek.fuzzywuzzy.Fuzz;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class ProcessPyTest {

    @Test
    void testExtractOne() {
        List<String> choices = Arrays.asList("new york jets", "new york giants", "liverpool");
        String query = "new york jets";
        Object[] res = Process.extractOne(query, choices);
        assertEquals("new york jets", res[0]);
    }

    @Test
    void testExtractLimitAndProcessor() {
        List<String> choices = Arrays.asList("foo Xbar", "bar", "baz");
        String query = "foo bar";
        List<Object[]> res = Process.extract(query, choices, 
                                             s -> s.toLowerCase(), 
                                             (a, b) -> Fuzz.tokenSortRatio((String)a, (String)b), 
                                             2);
        assertEquals(2, res.size());
    }

    @Test
    void testExtractNone() {
        assertNull(Process.extractOne(null, null));
        assertEquals(0, Process.extract(null, null).size());
    }

    @Test
    void testEmptyChoicesExtractOne() {
        assertNull(Process.extractOne("a", Collections.emptyList()));
        assertEquals(0, Process.extract("a", Collections.emptyList()).size());
    }

    @Test
    void testIndexedChoices() {
        Map<String, String> choices = new HashMap<>();
        choices.put("a", "foo");
        choices.put("b", "boo");
        Object[] out = Process.extractOne("foo", choices);
        assertEquals("foo", out[0]);
    }
}