package com.itsdangerous.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.Serializer;
import java.util.*;

public class SerializerPublicTest {

    @Test
    public void testDumpsAndLoads() {
        Serializer s = new Serializer("mys3cret");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("hello", "world");
        String dumped = s.dumps(data);
        assertNotNull(dumped);
        Map<String, Object> loaded = s.loads(dumped);
        assertEquals("world", loaded.get("hello"));
    }
}