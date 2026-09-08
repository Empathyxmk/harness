package com.facebook.sparts.public_;

import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicCollectionsExtraTest {
    @Test
    public void testPublicCollectionsExtraDummy() {
        List<Integer> lst = Arrays.asList(10, 2, 7, 4, 2);
        Set<Integer> s = new HashSet<>(lst);
        assertEquals(4, s.size());
        List<Integer> sorted = new ArrayList<>(s);
        Collections.sort(sorted);
        assertEquals(Arrays.asList(2, 4, 7, 10), sorted);
    }
}