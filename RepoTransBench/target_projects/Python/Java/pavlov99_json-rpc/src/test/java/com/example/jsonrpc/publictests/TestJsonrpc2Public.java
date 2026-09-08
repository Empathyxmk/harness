package com.example.jsonrpc.publictests;

import com.example.jsonrpc.jsonrpc2.JSONRPC2Request;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class TestJsonrpc2Public {

    @Test
    void testJsonrpc2PublicRequest() {
        JSONRPC2Request req = new JSONRPC2Request("baz", new Object[] {5,6}, 999);
        assertEquals("baz", req.getMethod());
        assertArrayEquals(new Object[] {5,6}, req.getArgs());
        assertEquals(999, req.getId());
    }
}