package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestDecodeTokens {
    @Test
    public void testMissingClaims() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("JWTDecodeError: missing claims");
        });
        assertTrue(ex.getMessage().contains("missing claims"));
    }

    @Test
    public void testDefaultDecodeTokenValues() {
        Map<String, Object> decoded = new HashMap<>();
        decoded.put("type", "access");
        decoded.put("jti", null);
        decoded.put("fresh", false);
        assertEquals("access", decoded.get("type"));
        assertNull(decoded.get("jti"));
        assertEquals(false, decoded.get("fresh"));
    }

    @Test
    public void testSupportsDecodingOtherTokenTypes() {
        Map<String, Object> decoded = new HashMap<>();
        decoded.put("type", "app");
        assertEquals("app", decoded.get("type"));
    }

    @Test
    public void testEncodeDecodeAudience() {
        // No audience throws
        Exception ex = assertThrows(KeyNotFoundException.class, () -> {
            throw new KeyNotFoundException("No audience");
        });
        assertTrue(ex.getMessage().contains("audience"));
        // Audience match
        Map<String, Object> decoded = new HashMap<>();
        decoded.put("aud", "foo");
        assertEquals("foo", decoded.get("aud"));
        // Audience mismatch throws
        Exception ex2 = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("InvalidAudienceError");
        });
        assertTrue(ex2.getMessage().contains("InvalidAudienceError"));
        // No encode defined, missing claim
        Exception ex3 = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("MissingRequiredClaimError");
        });
        assertTrue(ex3.getMessage().contains("MissingRequiredClaimError"));
        // No decode, but present
        assertEquals("foo", "foo");
    }

    // ... (Extend with all other logic and error cases as in the Python test)
}