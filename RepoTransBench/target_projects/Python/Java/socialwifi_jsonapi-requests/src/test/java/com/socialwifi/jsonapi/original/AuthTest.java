package com.socialwifi.jsonapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

public class AuthTest {

    static class TokenAuthentication {
        private String token;
        public TokenAuthentication(String token) { this.token = token; }
        public Map<String, String> authorizationHeader() {
            return Map.of("Authorization", "Bearer " + token);
        }
    }

    @Test
    public void testAuthorizationHeader() {
        TokenAuthentication auth = new TokenAuthentication("tok123");
        Map<String, String> headers = auth.authorizationHeader();
        assertTrue(headers.containsKey("Authorization"));
        assertEquals("Bearer tok123", headers.get("Authorization"));
    }

    @Test
    public void testAuthorizationHeaderWithDifferentToken() {
        TokenAuthentication auth = new TokenAuthentication("diffToken");
        Map<String, String> headers = auth.authorizationHeader();
        assertEquals("Bearer diffToken", headers.get("Authorization"));
    }
}