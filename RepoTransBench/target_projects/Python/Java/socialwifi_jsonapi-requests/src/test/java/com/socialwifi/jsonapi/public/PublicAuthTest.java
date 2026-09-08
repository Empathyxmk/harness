package com.socialwifi.jsonapi.public;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

public class PublicAuthTest {

    static class TokenAuth {
        String token;
        public TokenAuth(String token) { this.token = token; }
        public Map<String, String> getHeaders() {
            return Map.of("Authorization", "Bearer " + token);
        }
    }

    @Test
    public void testGetHeaders() {
        TokenAuth auth = new TokenAuth("s3cr3t");
        Map<String, String> headers = auth.getHeaders();
        assertTrue(headers.containsKey("Authorization"));
        assertEquals("Bearer s3cr3t", headers.get("Authorization"));
    }
}