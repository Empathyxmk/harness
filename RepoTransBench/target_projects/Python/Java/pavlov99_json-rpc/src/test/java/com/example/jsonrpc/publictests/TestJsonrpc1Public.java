package com.example.jsonrpc.publictests;

import com.example.jsonrpc.jsonrpc1.JSONRPC10Request;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class TestJsonrpc1Public {

    @Test
    void testPublicRequestFields() {
        JSONRPC10Request req = new JSONRPC10Request("foo", new Object[] {1,2}, 101);
        assertEquals("foo", req.getMethod());
        assertArrayEquals(new Object[] {1,2}, req.getArgs());
        assertEquals(101, req.getId());
    }

    @Test
    void testPublicRequestSerialize() throws Exception {
        JSONRPC10Request req = new JSONRPC10Request("bar", new Object[] {"a","b"}, 456);
        String json = req.toJson();
        assertTrue(json.contains("\"method\":\"bar\""));
        assertTrue(json.contains("\"id\":456"));
    }
}