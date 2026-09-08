package com.javaaid.search;

import static org.junit.Assert.assertEquals;

import java.util.Arrays;

import org.junit.Test;

public class TripleSumPublicTest {

    @Test
    public void testPublicInput1() {
        assertEquals(5, TripleSum.triplets(
            Arrays.asList(2, 3, 4, 4, 7),
            Arrays.asList(1, 2, 5, 5),
            Arrays.asList(3, 3, 5, 8)
        ));
    }

    @Test
    public void testPublicInput2() {
        assertEquals(9, TripleSum.triplets(
            Arrays.asList(3, 4, 7, 7, 10),
            Arrays.asList(1, 3, 5, 7, 9),
            Arrays.asList(2, 3, 6, 9)
        ));
    }
}