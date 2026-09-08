package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicCollectionsTest {
    @Test
    void testMapPublic() {
        List<Integer> input = Arrays.asList(4, 5, 6);
        List<Integer> expected = Arrays.asList(5, 6, 7);
        List<Integer> result = Underscore.map_(input, x -> x + 1);
        assertEquals(expected, result);
    }
}