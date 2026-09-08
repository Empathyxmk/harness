// Additional coverage for test_util.py.
package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestUtil {

    @Test
    void testDeserializeMap() {
        Map<String, Object> map = Map.of("foo", 42, "bar", "baz");
        String s = Util.serializeMap(map);
        Map<String, Object> deserialized = Util.deserializeMap(s);
        assertEquals(map, deserialized);
    }
}