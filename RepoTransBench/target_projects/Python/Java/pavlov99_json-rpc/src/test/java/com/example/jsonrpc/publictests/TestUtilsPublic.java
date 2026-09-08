package com.example.jsonrpc.publictests;

import com.example.jsonrpc.utils.MyJsonUtil;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class TestUtilsPublic {

    @Test
    void testJsonLoadsDictPublic() throws Exception {
        String json = "{\"name\": \"Alice\", \"count\": 5}";
        Map result = MyJsonUtil.loads(json);
        assertEquals("Alice", result.get("name"));
        assertEquals(5, result.get("count"));
    }
}