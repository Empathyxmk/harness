package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.*;

class PyLinqBranchTest {

    @Test
    void testBranchingEnumerables() {
        List<String> words = Arrays.asList("one", "two", "three", "four", "five");
        Stream<String> firstThree = words.stream().limit(3);
        Stream<String> lastTwo = words.stream().skip(3);
        List<String> a = firstThree.collect(Collectors.toList());
        List<String> b = lastTwo.collect(Collectors.toList());
        assertEquals(Arrays.asList("one", "two", "three"), a);
        assertEquals(Arrays.asList("four", "five"), b);
    }
}