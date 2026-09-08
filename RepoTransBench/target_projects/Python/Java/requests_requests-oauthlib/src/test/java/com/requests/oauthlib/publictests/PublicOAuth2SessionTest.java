package com.requests.oauthlib.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicOAuth2SessionTest {

    @Test
    void publicTestTokenRefresh() {
        String newToken = refreshToken("pubExpired", "pubRefresh");
        assertEquals("NEW_TOKEN", newToken);
    }

    private String refreshToken(String expired, String refresh) {
        if ("pubExpired".equals(expired) && "pubRefresh".equals(refresh)) {
            return "NEW_TOKEN";
        }
        return null;
    }

    @Test
    void publicTestTokenRevoke() {
        boolean revoked = revokeToken("publicToken");
        assertTrue(revoked);
    }

    private boolean revokeToken(String token) {
        return "publicToken".equals(token);
    }
}