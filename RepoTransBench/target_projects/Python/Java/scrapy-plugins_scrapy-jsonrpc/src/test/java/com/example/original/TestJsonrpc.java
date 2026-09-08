package com.example.original;

import com.example.jsonrpc.*;
import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

public class TestJsonrpc {

    public static class DummyTarget {
        public Object echo(Object x) { return x; }
        public Object add(Object a, Object b) {
            if (a instanceof Number && b instanceof Number) {
                return ((Number)a).intValue() + ((Number)b).intValue();
            }
            throw new IllegalArgumentException();
        }
        public Object fail() { throw new RuntimeException("fail!"); }
    }

    private static String makeReq(String method, Object params, Object id) throws Exception {
        Map<String, Object> d = new HashMap<>();
        d.put("jsonrpc", "2.0");
        d.put("method", method);
        d.put("id", id);
        if (params != null) {
            d.put("params", params);
        }
        return new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(d);
    }

    @Test
    void testJsonrpcResultErrorHelpers() {
        Map<String, Object> expected = new HashMap<>();
        expected.put("jsonrpc", "2.0");
        expected.put("result", java.util.Arrays.asList(1,2));
        expected.put("id", 17);
        assertEquals(expected, JsonRpcResult.jsonrpcResult(17, java.util.Arrays.asList(1,2)));

        Map<String, Object> e = JsonRpcResult.jsonrpcError(5, 1, "err", "trace");
        assertEquals(1, ((Map)e.get("error")).get("code"));
        assertEquals("trace", ((Map)e.get("error")).get("data"));
        assertEquals(5, e.get("id"));
    }

    @Test
    void testJsonrpcServerCallSuccessListParams() throws Exception {
        String req = makeReq("add", java.util.Arrays.asList(3,4), 1);
        Map<String, Object> result = JsonRpcServer.handle(new DummyTarget(), req);
        assertEquals(7, result.get("result"));
    }

    @Test
    void testJsonrpcServerCallSuccessDictParams() throws Exception {
        Map<String, Object> params = new HashMap<>();
        params.put("a", 10);
        params.put("b", 7);
        String req = makeReq("add", params, 1);
        Map<String, Object> result = JsonRpcServer.handle(new DummyTarget(), req);
        assertEquals(17, result.get("result"));
    }

    @Test
    void testJsonrpcServerCallSuccessEcho() throws Exception {
        String req = makeReq("echo", java.util.Collections.singletonList("hi"), 1);
        Map<String, Object> result = JsonRpcServer.handle(new DummyTarget(), req);
        assertEquals("hi", result.get("result"));
    }

    @Test
    void testJsonrpcServerCallInternalError() throws Exception {
        String req = makeReq("fail", null, 1);
        Map<String, Object> result = JsonRpcServer.handle(new DummyTarget(), req);
        assertEquals(JsonRpcErrors.INTERNAL_ERROR, ((Map)result.get("error")).get("code"));
        assertTrue(((Map)result.get("error")).get("message").toString().contains("fail!"));
    }

    @Test
    void testJsonrpcServerCallParseError() {
        class BadMapper extends com.fasterxml.jackson.databind.ObjectMapper {
            @Override public <T> T readValue(String content, Class<T> valueType) { throw new RuntimeException("parsefail"); }
        }
        Map<String, Object> result = JsonRpcServer.handle(new DummyTarget(), "badjson", new BadMapper());
        assertEquals(JsonRpcErrors.PARSE_ERROR, ((Map)result.get("error")).get("code"));
    }

    @Test
    void testJsonrpcServerCallInvalidRequest() throws Exception {
        String[] bads = new String[] {
                new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(Map.of("jsonrpc", "2.0")),
                new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(Map.of("jsonrpc", "2.0", "id", 1)),
                new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(Map.of("jsonrpc", "2.0", "method", "echo"))
        };
        for (String bad : bads) {
            Map<String, Object> result = JsonRpcServer.handle(new DummyTarget(), bad);
            assertEquals(JsonRpcErrors.INVALID_REQUEST, ((Map)result.get("error")).get("code"));
        }
    }

    @Test
    void testJsonrpcServerCallMethodNotFound() throws Exception {
        String req = makeReq("notfound", null, 1);
        Map<String, Object> result = JsonRpcServer.handle(new DummyTarget(), req);
        assertEquals(JsonRpcErrors.METHOD_NOT_FOUND, ((Map)result.get("error")).get("code"));
    }

    // Tests related to client call monkeypatch and exceptions are not directly portable.
}