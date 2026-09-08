package com.requests.oauthlib.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OAuth2AuthTest {

    @Test
    void testCreateAuthorizationUrl() {
        String url = buildAuthorizationUrl("https://auth.example.com", "clientid", "redirect", "state123");
        assertTrue(url.contains("redirect_uri=redirect"));
        assertTrue(url.contains("state=state123"));
    }

    private String buildAuthorizationUrl(String base, String clientId, String redirect, String state) {
        return base + "?client_id=" + clientId +
                "&redirect_uri=" + redirect +
                "&state=" + state;
    }

    @Test
    void testExchangeCodeForToken() {
        String token = exchangeCodeForToken("validCode");
        assertEquals("OAUTH2_TOKEN", token);
    }

    private String exchangeCodeForToken(String code) {
        if ("validCode".equals(code)) {
            return "OAUTH2_TOKEN";
        }
        return null;
    }
}