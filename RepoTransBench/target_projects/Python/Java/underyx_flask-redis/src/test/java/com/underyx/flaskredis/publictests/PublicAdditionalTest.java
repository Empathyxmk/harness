package com.underyx.flaskredis.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicAdditionalTest {
    @Test
    void testTruthPublic() {
        assertTrue(!"".equals("nonempty"), "Expected a non-empty string to evaluate as True");
    }

    @Test
    void testSplitStringPublic() {
        String s = "foo bar baz";
        String[] split = s.split("\\s+");
        assertArrayEquals(new String[]{"foo", "bar", "baz"}, split);
    }

    @Test
    void testSortedListPublic() {
        List<Integer> lst = Arrays.asList(10, 2, 4, 8);
        List<Integer> sorted = new ArrayList<>(lst);
        Collections.sort(sorted);
        assertEquals(Arrays.asList(2, 4, 8, 10), sorted);
    }

    @Test
    void testDictAccessPublic() {
        Map<String, Integer> d = new HashMap<>();
        d.put("alpha", 1); d.put("beta", 2);
        assertEquals(2, d.get("beta"));
        assertTrue(d.containsKey("alpha"));
    }
}