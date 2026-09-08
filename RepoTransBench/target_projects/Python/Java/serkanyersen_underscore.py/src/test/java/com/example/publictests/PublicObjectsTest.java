package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicObjectsTest {
    @Test
    void testKeysPublic() {
        Map<String, Integer> map = new HashMap<>();
        map.put("x", 42);
        map.put("y", 100);
        Set<String> expected = new HashSet<>(Arrays.asList("x", "y"));
        assertEquals(expected, Underscore.keys(map));
    }
}