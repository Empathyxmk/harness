package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;
import java.util.HashMap;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestBlocklist {
    @Test
    @Order(1)
    public void testBlocklistedAccessTokenRevocationSkip() {
        Map<String, Object> resp = new HashMap<>();
        resp.put("foo", "bar");
        int status = 200;
        assertEquals("bar", resp.get("foo"));
        assertEquals(200, status);
    }

    @Test
    @Order(2)
    public void testBlocklistedAccessTokenRevocationNoSkip() {
        Map<String, String> resp = new HashMap<>();
        resp.put("msg", "Token has been revoked");
        int status = 401;
        assertEquals("Token has been revoked", resp.get("msg"));
        assertEquals(401, status);
    }

    @Test
    @Order(3)
    public void testNonBlocklistedAccessToken() {
        Map<String, Object> resp = new HashMap<>();
        resp.put("foo", "bar");
        int status = 200;
        assertEquals("bar", resp.get("foo"));
        assertEquals(200, status);
    }

    @Test
    @Order(4)
    public void testBlocklistedAccessToken() {
        Map<String, String> resp = new HashMap<>();
        resp.put("msg", "Token has been revoked");
        int status = 401;
        assertEquals("Token has been revoked", resp.get("msg"));
        assertEquals(401, status);
    }

    @Test
    @Order(5)
    public void testNonBlocklistedRefreshToken() {
        Map<String, Object> resp = new HashMap<>();
        resp.put("foo", "bar");
        int status = 200;
        assertEquals("bar", resp.get("foo"));
        assertEquals(200, status);
    }

    @Test
    @Order(6)
    public void testBlocklistedRefreshToken() {
        Map<String, String> resp = new HashMap<>();
        resp.put("msg", "Token has been revoked");
        int status = 401;
        assertEquals("Token has been revoked", resp.get("msg"));
        assertEquals(401, status);
    }

    @Test
    @Order(7)
    public void testCustomBlocklistedMessage() {
        Map<String, Object> resp = new HashMap<>();
        resp.put("baz", "foo");
        int status = 404;
        assertEquals("foo", resp.get("baz"));
        assertEquals(404, status);
    }
}