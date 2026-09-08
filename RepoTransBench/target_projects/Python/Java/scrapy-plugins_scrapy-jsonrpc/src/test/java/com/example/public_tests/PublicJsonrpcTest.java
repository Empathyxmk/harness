package com.example.public_tests;

import org.junit.jupiter.api.Test;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class PublicJsonrpcTest {

    public static Map<String,Object> jsonrpcSuccessObj(Object id, Object result) {
        return java.util.Map.of("jsonrpc", "2.0", "id", id, "result", result);
    }

    public static Map<String,Object> jsonrpcErrorObj(Object id, int code, String message) {
        return java.util.Map.of("jsonrpc", "2.0", "id", id, "error",
                java.util.Map.of("code", code, "message", message));
    }

    public static Map<String,Object> jsonrpcErrorObj(Object id, int code, String message, Map<String, Object> data) {
        return java.util.Map.of("jsonrpc", "2.0", "id", id, "error",
                java.util.Map.of("code", code, "message", message, "data", data));
    }

    @Test
    void testJsonrpcSuccessObjPublic() {
        Map<String,Object> result = jsonrpcSuccessObj("abcde", java.util.Map.of("value", 99));
        assertEquals("2.0", result.get("jsonrpc"));
        assertEquals("abcde", result.get("id"));
        assertEquals(java.util.Map.of("value", 99), result.get("result"));
    }

    @Test
    void testJsonrpcErrorObjPublic() {
        Map<String,Object> error = jsonrpcErrorObj("xyz01", -123, "Unexpected Error");
        assertEquals("2.0", error.get("jsonrpc"));
        assertEquals("xyz01", error.get("id"));
        Map<String,Object> err = (Map<String,Object>) error.get("error");
        assertEquals(-123, err.get("code"));
        assertEquals("Unexpected Error", err.get("message"));
    }

    @Test
    void testJsonrpcErrorObjWithDataPublic() {
        Map<String,Object> error = jsonrpcErrorObj("ab10", -20, "Message", java.util.Map.of("details", "extra"));
        assertEquals("2.0", error.get("jsonrpc"));
        assertEquals("ab10", error.get("id"));
        Map<String,Object> err = (Map<String,Object>) error.get("error");
        assertEquals(-20, err.get("code"));
        assertEquals("Message", err.get("message"));
        assertEquals(java.util.Map.of("details", "extra"), err.get("data"));
    }
}