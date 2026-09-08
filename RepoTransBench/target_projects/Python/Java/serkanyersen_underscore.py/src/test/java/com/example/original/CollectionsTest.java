package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CollectionsTest {
    @Test
    void testMap() {
        List<Integer> input = Arrays.asList(1, 2, 3);
        List<Integer> expected = Arrays.asList(2, 4, 6);
        List<Integer> result = Underscore.map_(input, x -> x * 2);
        assertEquals(expected, result);
    }
}