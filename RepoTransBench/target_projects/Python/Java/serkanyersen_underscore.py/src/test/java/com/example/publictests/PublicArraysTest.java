package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicArraysTest {
    @Test
    void testChunkPublic() {
        List<Integer> input = Arrays.asList(10, 20, 30, 40, 50);
        List<List<Integer>> expected = Arrays.asList(
                Arrays.asList(10, 20, 30),
                Arrays.asList(40, 50)
        );
        assertEquals(expected, Underscore.chunk(input, 3));
    }

    @Test
    void testCompactPublic() {
        List<Object> input = Arrays.asList(null, "hello", "", 0, 9, false, 5);
        List<Object> expected = Arrays.asList("hello", 9, 5);
        assertEquals(expected, Underscore.compact(input));
    }
}