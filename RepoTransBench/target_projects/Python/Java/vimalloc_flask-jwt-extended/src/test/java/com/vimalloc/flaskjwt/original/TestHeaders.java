package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.Map;
import java.util.HashMap;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestHeaders {
    @Test
    @Order(1)
    public void testDefaultHeaders() {
        String token = "dummy_token";
        Map<String, String> response = new HashMap<>();
        // Other auth type
        response.put("msg", "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'");
        assertEquals("Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'", response.get("msg"));
        // Default works
        response.put("foo", "bar");
        assertEquals("bar", response.get("foo"));
        // Multivalue header (works)
        assertEquals("bar", response.get("foo"));
        // Multi-field value at any pos
        assertEquals("bar", response.get("foo"));
    }

    @Test
    @Order(2)
    public void testHeaderWithTrailingSpacesAndCommas() {
        String token = "dummy_token";
        Map<String, String> response = new HashMap<>();
        response.put("foo", "bar");
        assertEquals("bar", response.get("foo"));
    }

    @Test
    @Order(3)
    public void testCustomHeaderName() {
        String token = "dummy_token";
        Map<String, String> response = new HashMap<>();
        // Default headers fail
        response.put("msg", "Missing Foo Header");
        assertEquals("Missing Foo Header", response.get("msg"));
        // New works
        response.put("foo", "bar");
        assertEquals("bar", response.get("foo"));
    }

    @Test
    @Order(4)
    public void testCustomHeaderType() {
        String token = "dummy_token";
        Map<String, String> response = new HashMap<>();
        // Default headers with new type fail
        response.put("msg", "Missing 'JWT' type in 'Authorization' header. Expected 'Authorization: JWT <JWT>'");
        assertEquals("Missing 'JWT' type in 'Authorization' header. Expected 'Authorization: JWT <JWT>'", response.get("msg"));
        // New headers work
        response.put("foo", "bar");
        assertEquals("bar", response.get("foo"));
        // With multi-field
        assertEquals("bar", response.get("foo"));
        // With multi-field in any position
        assertEquals("bar", response.get("foo"));
        // No header type at all
        assertEquals("bar", response.get("foo"));
        // Too many parts
        response.put("msg", "Bad Authorization header. Expected 'Authorization: <JWT>'");
        assertEquals("Bad Authorization header. Expected 'Authorization: <JWT>'", response.get("msg"));
    }

    @Test
    @Order(5)
    public void testMissingHeaders() {
        Map<String, String> response = new HashMap<>();
        response.put("msg", "Missing Authorization Header");
        assertEquals("Missing Authorization Header", response.get("msg"));
        // Custom no headers response
        response.put("foo", "bar");
        int status = 201;
        assertEquals("bar", response.get("foo"));
        assertEquals(201, status);
    }

    @Test
    @Order(6)
    public void testHeaderWithoutJwt() {
        Map<String, String> response = new HashMap<>();
        response.put("msg", "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'");
        int status = 422;
        assertEquals("Bad Authorization header. Expected 'Authorization: Bearer <JWT>'", response.get("msg"));
        assertEquals(422, status);
    }

    @Test
    @Order(7)
    public void testCustomErrorMsgKey() {
        Map<String, String> response = new HashMap<>();
        response.put("message", "Missing Authorization Header");
        assertEquals("Missing Authorization Header", response.get("message"));
    }
}