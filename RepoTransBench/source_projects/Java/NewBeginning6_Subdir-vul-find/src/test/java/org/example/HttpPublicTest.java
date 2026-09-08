package org.example;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.*;

public class HttpPublicTest {

    @Test
    void testResponseShape() {
        // Instead of a real call, use obviously invalid URL and test structure/shape of list
        String url = "http://example.invalid";
        String cookie = "mycookie=12345";
        String ua = "PublicAgent/2.0";
        String xHeaders = "X-Test: public\nTest-Header: 42";
        String method = "get";
        String dataBody = "";
        String enctypeBody = "application/json";
        boolean follow = false;

        try {
            ArrayList response = Http.Response(url, cookie, ua, xHeaders, method, dataBody, enctypeBody, follow);
            assertNotNull(response);
            assertTrue(response.size() >= 4);
        } catch(Exception e) {
            // Should not throw exception, but if it does, at least catch and fail properly
            fail("Http.Response() threw: " + e);
        }
    }
}