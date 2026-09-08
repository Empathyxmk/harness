package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicDecoratorsTest {

    @Test
    void testSortPublic() {
        List<Integer> xs = Arrays.asList(3,1,2);
        List<Integer> sorted = new ArrayList<>(xs);
        sorted.sort(Comparator.naturalOrder());
        assertEquals(Arrays.asList(1,2,3), sorted);
    }
}