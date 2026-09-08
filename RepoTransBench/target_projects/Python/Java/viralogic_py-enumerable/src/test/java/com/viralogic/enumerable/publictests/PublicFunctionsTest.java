package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.Collectors;

class PublicFunctionsTest {

    @Test
    void testDistinctPublic() {
        List<String> vals = Arrays.asList("a", "a", "b", "b", "c");
        List<String> distinct = vals.stream().distinct().collect(Collectors.toList());
        assertEquals(Arrays.asList("a","b","c"), distinct);
    }

    @Test
    void testReversePublic() {
        List<Integer> ne = Arrays.asList(5,4,3,2,1);
        List<Integer> copy = new ArrayList<>(ne);
        Collections.reverse(copy);
        assertEquals(Arrays.asList(1,2,3,4,5), copy);
    }
}