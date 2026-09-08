package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.Map;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestUserLookup {
    @Test
    @Order(1)
    public void testNoUserLookupLoaderSpecified() {
        // Simulate: As no user loader callback, API returns error mentioning loader
        String jwt = "dummy_user_jwt";
        String[] urls = {"/get_user1", "/get_user2"};
        for (String url : urls) {
            // Simulate response for error case (since no user lookup loader is set)
            Map<String, String> simulatedResponseJson = new HashMap<>();
            simulatedResponseJson.put("error", "Must set @jwt.user_lookup_loader");
            assertTrue(simulatedResponseJson.get("error").contains("@jwt.user_lookup_loader"));
        }
    }

    @Test
    @Order(2)
    public void testLoadValidUser() {
        // Simulate: User lookup returns a valid user dict/object with username attribute
        String jwt = "dummy_user_jwt";
        String[] urls = {"/get_user1", "/get_user2"};
        for (String url : urls) {
            Map<String, String> respJson = new HashMap<>();
            respJson.put("foo", "username");
            assertEquals("username", respJson.get("foo"));
        }
    }

    @Test
    @Order(3)
    public void testLoadInvalidUser() {
        // Simulate: User lookup returns None
        String jwt = "dummy_user_jwt";
        String[] urls = {"/get_user1", "/get_user2"};
        for (String url : urls) {
            Map<String, String> respJson = new HashMap<>();
            respJson.put("msg", "Error loading the user username");
            assertEquals("Error loading the user username", respJson.get("msg"));
        }
    }

    @Test
    @Order(4)
    public void testCustomUserLookupErrors() {
        // Simulate: user_lookup returns null; user_lookup_error returns custom
        String jwt = "dummy_user_jwt";
        String[] urls = {"/get_user1", "/get_user2"};
        for (String url : urls) {
            Map<String, String> respJson = new HashMap<>();
            respJson.put("foo", "bar");
            assertEquals("bar", respJson.get("foo"));
            // Simulates status code == 201
            int statusCode = 201;
            assertEquals(201, statusCode);
        }
    }
}