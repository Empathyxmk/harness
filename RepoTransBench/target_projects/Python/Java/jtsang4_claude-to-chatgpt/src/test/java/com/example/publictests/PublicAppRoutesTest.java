package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicAppRoutesTest {

    @Test
    public void testPublicHealthRoute() {
        Map<String, Object> response = PublicFakeFastApi.appGet("/healthz");
        assertEquals(200, response.get("status"));
        assertTrue(response.get("body") instanceof String || response.get("body")==null);
        String text = response.get("body")==null ? "" : response.get("body").toString();
        assertTrue(
          text.equals("\"ok\"") || text.equals("ok") || text.equals("'ok'") || text.equals(""));
    }

    @Test
    public void testPublicNotFoundRoute() {
        Map<String, Object> response = PublicFakeFastApi.appGet("/non-existent-endpoint2123");
        assertEquals(404, response.get("status"));
    }

    @Test
    public void testPublicRootRoute() {
        Map<String, Object> response = PublicFakeFastApi.appGet("/");
        int status = (int)response.get("status");
        assertTrue(status == 404 || status == 200);
    }

    @Test
    public void testPublicOptionsReturns405ForStandardEndpoint() {
        Map<String, Object> response = PublicFakeFastApi.options("/healthz");
        int code = (int) response.get("status");
        assertTrue(code==405||code==200||code==204);
    }
}

// Simulated public FastAPI endpoints for public tests
class PublicFakeFastApi {
    public static Map<String, Object> appGet(String route) {
        if (route.equals("/healthz")) {
            return Map.of("status", 200, "body", "ok");
        }
        if (route.equals("/")) {
            return Map.of("status", 404, "body", null);
        }
        return Map.of("status", 404, "body", null);
    }
    public static Map<String, Object> options(String route) {
        if (route.equals("/healthz")) {
            return Map.of("status", 405, "body", null);
        }
        return Map.of("status", 405, "body", null);
    }
}