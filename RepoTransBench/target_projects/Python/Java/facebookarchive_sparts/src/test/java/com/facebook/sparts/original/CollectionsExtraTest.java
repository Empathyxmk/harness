package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class CollectionsExtraTest {
    @Test
    public void testCollectionsExtraDummy() {
        List<Integer> lst = Arrays.asList(10, 3, 7, 5, 2, 4, 2);
        Set<Integer> s = new HashSet<>(lst);
        assertEquals(6, s.size());
        List<Integer> sorted = new ArrayList<>(s);
        Collections.sort(sorted);
        assertEquals(Arrays.asList(2, 3, 4, 5, 7, 10), sorted);
    }
}