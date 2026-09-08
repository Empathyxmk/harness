package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class ObjectsTest {
    @Test
    void testKeys() {
        Map<String, Integer> map = new HashMap<>();
        map.put("a", 1);
        map.put("b", 2);
        Set<String> keys = Underscore.keys(map);
        assertEquals(new HashSet<>(Arrays.asList("a", "b")), keys);
    }
}