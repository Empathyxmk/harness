package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicMoreCoverageTest {
    @Test
    void testIsEmptyPublic() {
        assertTrue(Underscore.is_empty(new HashMap<>()));
        Map<String, String> map = new HashMap<>();
        map.put("a", "z");
        assertFalse(Underscore.is_empty(map));
    }
}