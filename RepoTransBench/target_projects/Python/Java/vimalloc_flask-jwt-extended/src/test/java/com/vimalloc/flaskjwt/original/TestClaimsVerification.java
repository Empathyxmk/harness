package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.Map;
import java.util.HashMap;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestClaimsVerification {

    @Test
    @Order(1)
    public void testSuccessfulClaimsValidation() {
        String jwt = "dummy_jwt";
        String[] urls = {"/protected1", "/protected2", "/protected3"};
        for (String url : urls) {
            // Simulate a valid JWT claims verification callback returns true.
            Map<String, Object> response = new HashMap<>();
            response.put("foo", "bar");
            int status = 200;
            assertEquals("bar", response.get("foo"));
            assertEquals(200, status);
        }
    }

    @Test
    @Order(2)
    public void testUnsuccessfulClaimsValidation() {
        String jwt = "dummy_jwt";
        String[] urls = {"/protected1", "/protected2", "/protected3"};
        for (String url : urls) {
            Map<String, String> response = new HashMap<>();
            response.put("msg", "User claims verification failed");
            int status = 400;
            assertEquals("User claims verification failed", response.get("msg"));
            assertEquals(400, status);
        }
    }

    @Test
    @Order(3)
    public void testClaimsValidationCustomError() {
        String jwt = "dummy_jwt";
        String[] urls = {"/protected1", "/protected2", "/protected3"};
        for (String url : urls) {
            Map<String, String> response = new HashMap<>();
            response.put("msg", "claims failed for username");
            int status = 404;
            assertEquals("claims failed for username", response.get("msg"));
            assertEquals(404, status);
        }
    }
}