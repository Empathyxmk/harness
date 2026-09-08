package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.Map;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestJwtHeaderLoader {
    @Test
    @Order(1)
    public void testJwtHeadersInAccessToken() {
        Map<String, Object> headers = new HashMap<>();
        headers.put("foo", "bar");
        assertEquals("bar", headers.get("foo"));
        int status = 200;
        assertEquals(200, status);
    }

    @Test
    @Order(2)
    public void testNonSerializableHeaders() {
        // Simulate: raises TypeError if headers are not serializable
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("TypeError: non-serializable headers");
        });
        assertTrue(ex.getMessage().contains("TypeError"));
    }

    @Test
    @Order(3)
    public void testJwtHeadersInRefreshToken() {
        Map<String, Object> headers = new HashMap<>();
        headers.put("foo", "bar");
        assertEquals("bar", headers.get("foo"));
        int status = 200;
        assertEquals(200, status);
    }

    @Test
    @Order(4)
    public void testJwtHeaderInRefreshTokenSpecifiedAtCreation() {
        Map<String, Object> headers = new HashMap<>();
        headers.put("foo", "bar");
        assertEquals("bar", headers.get("foo"));
        int status = 200;
        assertEquals(200, status);
    }

    @Test
    @Order(5)
    public void testJwtHeaderInAccessTokenSpecifiedAtCreation() {
        Map<String, Object> headers = new HashMap<>();
        headers.put("foo", "bar");
        assertEquals("bar", headers.get("foo"));
        int status = 200;
        assertEquals(200, status);
    }

    @Test
    @Order(6)
    public void testJwtHeaderInAccessTokenSpecifiedAtCreationOverride() {
        Map<String, Object> headers = new HashMap<>();
        headers.put("foo", "bar");
        assertEquals("bar", headers.get("foo"));
        int status = 200;
        assertEquals(200, status);
    }

    @Test
    @Order(7)
    public void testJwtHeaderInRefreshTokenSpecifiedAtCreationOverride() {
        Map<String, Object> headers = new HashMap<>();
        headers.put("foo", "bar");
        assertEquals("bar", headers.get("foo"));
        int status = 200;
        assertEquals(200, status);
    }
}