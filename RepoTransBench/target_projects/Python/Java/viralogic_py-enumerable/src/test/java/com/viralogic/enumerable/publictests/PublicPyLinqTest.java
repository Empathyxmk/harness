package com.viralogic.enumerable.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.util.stream.Collectors;

class PublicPyLinqTest {

    @Test
    void testChainedOperations() {
        List<Integer> xs = Arrays.asList(2,3,4,5,6);
        List<Integer> oddSquares = xs.stream().filter(x -> x%2 == 1)
            .map(x -> x * x)
            .collect(Collectors.toList());
        assertEquals(Arrays.asList(9, 25), oddSquares);
    }
}