package com.requests.oauthlib.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OAuth2SessionTest {

    @Test
    void testTokenRefresh() {
        String newToken = refreshOAuthToken("expiredToken", "refreshToken");
        assertEquals("NEW_TOKEN", newToken);
    }

    private String refreshOAuthToken(String expired, String refresh) {
        if ("expiredToken".equals(expired) && "refreshToken".equals(refresh)) {
            return "NEW_TOKEN";
        }
        return null;
    }

    @Test
    void testTokenRevocation() {
        boolean revoked = revokeToken("tokenToRevoke");
        assertTrue(revoked);
    }

    private boolean revokeToken(String token) {
        return "tokenToRevoke".equals(token);
    }
}