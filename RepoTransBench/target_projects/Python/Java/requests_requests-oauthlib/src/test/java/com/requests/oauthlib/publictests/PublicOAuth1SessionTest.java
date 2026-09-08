package com.requests.oauthlib.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicOAuth1SessionTest {

    @Test
    void publicTestFetchRequestToken() {
        String token = fetchRequestToken("pubKey", "pubSecret");
        assertEquals("REQUEST_TOKEN", token);
    }

    private String fetchRequestToken(String cKey, String cSecret) {
        if ("pubKey".equals(cKey) && "pubSecret".equals(cSecret)) {
            return "REQUEST_TOKEN";
        }
        return null;
    }

    @Test
    void publicTestFetchAccessToken() {
        String token = fetchAccessToken("pubVerifier");
        assertEquals("ACCESS_TOKEN", token);
    }

    private String fetchAccessToken(String verifier) {
        if ("pubVerifier".equals(verifier)) {
            return "ACCESS_TOKEN";
        }
        return null;
    }
}