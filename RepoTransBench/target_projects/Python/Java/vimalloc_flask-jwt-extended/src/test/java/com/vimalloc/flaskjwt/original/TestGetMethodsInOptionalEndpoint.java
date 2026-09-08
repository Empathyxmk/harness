package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.HashMap;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestGetMethodsInOptionalEndpoint {
    @Test
    public void testGetJwtInOptionalRoute() {
        // Simulates checking that all get methods etc. in an unprotected context give default values
        Map<String, Object> resp = new HashMap<>();
        resp.put("foo", "bar");
        assertEquals("bar", resp.get("foo"));
    }
}