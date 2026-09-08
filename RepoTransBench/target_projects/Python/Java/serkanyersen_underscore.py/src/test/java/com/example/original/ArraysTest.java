package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class ArraysTest {
    @Test
    void testChunk() {
        List<Integer> input = Arrays.asList(1, 2, 3, 4);
        List<List<Integer>> result = Underscore.chunk(input, 2);
        List<List<Integer>> expected = Arrays.asList(
                Arrays.asList(1, 2),
                Arrays.asList(3, 4)
        );
        assertEquals(expected, result);
    }

    @Test
    void testCompact() {
        List<Object> input = Arrays.asList(0, 1, false, 2, "", 3);
        List<Object> expected = Arrays.asList(1, 2, 3);
        List<Object> result = Underscore.compact(input);
        assertEquals(expected, result);
    }
}