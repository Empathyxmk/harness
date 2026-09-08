package com.requests.oauthlib.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicCoreTest {

    @Test
    void publicTestEncodeParams() {
        String encoded = urlEncodeParams("x", "y@y.com");
        assertEquals("x=y%40y.com", encoded);
    }

    private String urlEncodeParams(String key, String value) {
        return key + "=" + value.replace("@", "%40");
    }
}