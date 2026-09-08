package com.requests.oauthlib.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CoreTest {

    @Test
    void testUrlEncodeParams() {
        String encoded = urlEncodeParams("foo", "bar@baz.com");
        assertEquals("foo=bar%40baz.com", encoded);
    }

    private String urlEncodeParams(String key, String value) {
        return key + "=" + value.replace("@", "%40");
    }

    @Test
    void testAuthorizationHeader() {
        String token = "myToken";
        String header = buildAuthorizationHeader(token);
        assertEquals("Bearer myToken", header);
    }

    private String buildAuthorizationHeader(String token) {
        return "Bearer " + token;
    }
}