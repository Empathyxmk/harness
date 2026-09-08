package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class UtilTest {

    @Test
    void testSerializeMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("a", 3);
        map.put("b", "z");
        String s = Util.serializeMap(map);
        assertTrue(s.contains("a") && s.contains("b"));
    }
}