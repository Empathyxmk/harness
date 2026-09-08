package com.requests.oauthlib.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicInitAndSetupTest {

    @Test
    void publicTestInitDefault() {
        OAuthSession session = new OAuthSession();
        assertNotNull(session);
    }

    static class OAuthSession {}

    @Test
    void publicTestInitWithParams() {
        OAuthSession session = new OAuthSession("pubId", "pubSecret");
        assertEquals("pubId", session.clientId);
        assertEquals("pubSecret", session.clientSecret);
    }

    static class OAuthSession {
        String clientId;
        String clientSecret;
        OAuthSession() {}
        OAuthSession(String clientId, String clientSecret) {
            this.clientId = clientId;
            this.clientSecret = clientSecret;
        }
    }
}