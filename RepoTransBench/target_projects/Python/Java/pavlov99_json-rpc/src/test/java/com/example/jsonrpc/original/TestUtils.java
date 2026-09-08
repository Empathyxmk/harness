package com.example.jsonrpc.original;

import com.example.jsonrpc.utils.MyJsonUtil;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class TestUtils {

    @Test
    void testJsonLoadsValidObject() throws Exception {
        String json = "{\"a\": 1, \"b\": [1,2,3]}";
        Map result = MyJsonUtil.loads(json);
        assertEquals(1, result.get("a"));
        assertEquals(Arrays.asList(1,2,3), result.get("b"));
    }

    @Test
    void testJsonLoadsInvalidThrows() {
        String invalidJson = "{a: 1, b: 2}";
        assertThrows(Exception.class, () -> MyJsonUtil.loads(invalidJson));
    }

    @Test
    void testJsonDumpsMap() throws Exception {
        Map<String, Object> data = new HashMap<>();
        data.put("foo", 123);
        data.put("bar", Arrays.asList(1, 2, 3));
        String json = MyJsonUtil.dumps(data);
        assertTrue(json.contains("\"foo\""));
        assertTrue(json.contains("123"));
    }
}