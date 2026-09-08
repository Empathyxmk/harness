package com.requests.oauthlib.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OAuth1SessionTest {

    @Test
    void testFetchRequestToken() {
        String token = fetchRequestToken("consumerKey", "consumerSecret");
        assertEquals("REQUEST_TOKEN", token);
    }

    private String fetchRequestToken(String consumerKey, String consumerSecret) {
        // Mocked: pretend to talk to server
        if ("consumerKey".equals(consumerKey) && "consumerSecret".equals(consumerSecret)) {
            return "REQUEST_TOKEN";
        }
        return null;
    }

    @Test
    void testFetchAccessToken() {
        String token = fetchAccessToken("verifierCode");
        assertEquals("ACCESS_TOKEN", token);
    }

    private String fetchAccessToken(String verifier) {
        if ("verifierCode".equals(verifier)) {
            return "ACCESS_TOKEN";
        }
        return null;
    }
}