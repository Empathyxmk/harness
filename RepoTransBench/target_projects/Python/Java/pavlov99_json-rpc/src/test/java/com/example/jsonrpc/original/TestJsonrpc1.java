package com.example.jsonrpc.original;

import com.example.jsonrpc.jsonrpc1.JSONRPC10Request;
import com.example.jsonrpc.jsonrpc1.JSONRPC10Response;
import com.example.jsonrpc.exceptions.JSONRPCInvalidRequestException;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class TestJsonrpc1 {

    @Test
    void testRequestCreation() {
        JSONRPC10Request req = new JSONRPC10Request("sum", Arrays.asList(1, 2, 3), 123);
        assertEquals("sum", req.getMethod());
        assertEquals(Arrays.asList(1,2,3), req.getParams());
        assertEquals(123, req.getId());
    }

    @Test
    void testRequestToJson() throws Exception {
        JSONRPC10Request req = new JSONRPC10Request("sum", Arrays.asList(1, 2, 3), 123);
        String json = req.toJson();
        ObjectMapper mapper = new ObjectMapper();
        Map parsed = mapper.readValue(json, Map.class);
        assertEquals("sum", parsed.get("method"));
        assertEquals(Arrays.asList(1,2,3), parsed.get("params"));
        assertEquals(123, parsed.get("id"));
    }

    @Test
    void testRequestFromJson() throws Exception {
        String json = "{\"method\": \"sum\", \"params\": [1, 2], \"id\": 12}";
        JSONRPC10Request req = JSONRPC10Request.fromJson(json);
        assertEquals("sum", req.getMethod());
        assertEquals(Arrays.asList(1,2), req.getParams());
        assertEquals(12, req.getId());
    }

    @Test
    void testResponseCreation() {
        JSONRPC10Response resp = new JSONRPC10Response(123, null, "ok");
        assertEquals(123, resp.getId());
        assertNull(resp.getError());
        assertEquals("ok", resp.getResult());
    }

    @Test
    void testResponseToJson() throws Exception {
        JSONRPC10Response resp = new JSONRPC10Response(123, null, "ok");
        String json = resp.toJson();
        ObjectMapper mapper = new ObjectMapper();
        Map parsed = mapper.readValue(json, Map.class);
        assertEquals(123, parsed.get("id"));
        assertNull(parsed.get("error"));
        assertEquals("ok", parsed.get("result"));
    }

    @Test
    void testResponseFromJson() throws Exception {
        String json = "{\"id\": 1, \"result\": 42, \"error\": null}";
        JSONRPC10Response resp = JSONRPC10Response.fromJson(json);
        assertEquals(1, resp.getId());
        assertEquals(42, resp.getResult());
        assertNull(resp.getError());
    }

    @Test
    void testRequestValidationError() {
        assertThrows(IllegalArgumentException.class, () ->
            new JSONRPC10Request(null, Arrays.asList(1,2), 1)
        );
        assertThrows(IllegalArgumentException.class, () ->
            new JSONRPC10Request("foo", null, 1)
        );
    }

    @Test
    void testResponseValidationError() {
        assertThrows(IllegalArgumentException.class, () ->
            new JSONRPC10Response(null, "err", null)
        );
    }
}