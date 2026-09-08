package com.requests.oauthlib.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicOAuth2AuthTest {

    @Test
    void publicTestAuthorizeUrl() {
        String url = buildAuthorizeUrl("https://example.com", "pubid", "redir", "s789");
        assertTrue(url.contains("redirect_uri=redir"));
        assertTrue(url.contains("state=s789"));
    }

    private String buildAuthorizeUrl(String base, String id, String redirect, String state) {
        return base + "?client_id=" + id +
                "&redirect_uri=" + redirect +
                "&state=" + state;
    }

    @Test
    void publicTestExchangeToken() {
        String token = exchangeToken("goodCode");
        assertEquals("OAUTH2_TOKEN", token);
    }

    private String exchangeToken(String code) {
        if ("goodCode".equals(code)) {
            return "OAUTH2_TOKEN";
        }
        return null;
    }
}