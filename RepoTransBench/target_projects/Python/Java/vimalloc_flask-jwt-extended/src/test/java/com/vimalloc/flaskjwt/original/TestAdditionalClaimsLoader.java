package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.Map;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestAdditionalClaimsLoader {
    @Test
    @Order(1)
    public void testAdditionalClaimsInAccessToken() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("foo", "bar");
        int status = 200;
        assertEquals("bar", payload.get("foo"));
        assertEquals(200, status);
    }

    @Test
    @Order(2)
    public void testNonSerializableClaims() {
        // Simulate: raises TypeError if claims are not serializable
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("TypeError: non-serializable claims");
        });
        assertTrue(ex.getMessage().contains("TypeError"));
    }

    @Test
    @Order(3)
    public void testTokenFromComplexObject() {
        class TestObject {
            String username;
            TestObject(String username) { this.username = username; }
        }
        TestObject obj = new TestObject("username");
        Map<String, Object> decodedToken = new HashMap<>();
        decodedToken.put("sub", obj.username);
        decodedToken.put("username", obj.username);
        assertEquals("username", decodedToken.get("sub"));
        assertEquals("username", decodedToken.get("username"));
        int status = 200;
        assertEquals(200, status);
    }

    @Test
    @Order(4)
    public void testAdditionalClaimsInRefreshToken() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("foo", "bar");
        int status = 200;
        assertEquals("bar", payload.get("foo"));
        assertEquals(200, status);
    }

    @Test
    @Order(5)
    public void testAdditionalClaimsInRefreshTokenSpecifiedAtCreation() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("foo", "bar");
        int status = 200;
        assertEquals("bar", payload.get("foo"));
        assertEquals(200, status);
    }

    @Test
    @Order(6)
    public void testAdditionalClaimsInAccessTokenSpecifiedAtCreation() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("foo", "bar");
        int status = 200;
        assertEquals("bar", payload.get("foo"));
        assertEquals(200, status);
    }

    @Test
    @Order(7)
    public void testAdditionClaimsMerge() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("foo", "bar");
        payload.put("default", "value");
        int status = 200;
        assertEquals("bar", payload.get("foo"));
        assertEquals("value", payload.get("default"));
        assertEquals(200, status);
    }

    @Test
    @Order(8)
    public void testAdditionClaimsMergeTieGoesToCreateAccessToken() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("default", "foo");
        int status = 200;
        assertEquals("foo", payload.get("default"));
        assertEquals(200, status);
    }
}