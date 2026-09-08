package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class MoreCoverageTest {
    @Test
    void testIsEmpty() {
        assertTrue(Underscore.is_empty(Collections.emptyList()));
        assertFalse(Underscore.is_empty(Arrays.asList(1)));
    }
}