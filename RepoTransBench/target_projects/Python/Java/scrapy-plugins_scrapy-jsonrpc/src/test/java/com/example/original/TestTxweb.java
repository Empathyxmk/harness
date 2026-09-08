package com.example.original;

import com.example.txweb.JsonResource;
import com.example.txweb.DummyRequest;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestTxweb {

    @Test
    void testJsonResourceRenderObjectSetsHeadersAndReturnsJson() throws Exception {
        JsonResource jr = new JsonResource();
        DummyRequest dr = new DummyRequest();
        java.util.Map<String, Object> obj = new java.util.HashMap<>();
        obj.put("foo", "bar");
        String res = jr.renderObject(obj, dr);
        assertTrue(res.trim().startsWith("{") && res.trim().endsWith("}"));
        assertTrue(res.contains("\"foo\":\"bar\"") || res.contains("\"foo\": \"bar\""));
        assertEquals("application/json", dr._headers.get("Content-Type"));
        assertEquals("*", dr._headers.get("Access-Control-Allow-Origin"));
        assertEquals("GET, POST, PATCH, PUT, DELETE", dr._headers.get("Access-Control-Allow-Methods"));
        assertEquals(" X-Requested-With", dr._headers.get("Access-Control-Allow-Headers"));
        assertEquals(res.length(), dr._headers.get("Content-Length"));
    }
}