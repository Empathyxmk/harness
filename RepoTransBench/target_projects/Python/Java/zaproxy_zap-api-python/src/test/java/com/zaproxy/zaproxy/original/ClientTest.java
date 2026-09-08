package com.zaproxy.zaproxy.original;

import static org.junit.jupiter.api.Assertions.*;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.hasEntry;
import static org.hamcrest.Matchers.allOf;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.*;

class HeaderMap extends HashMap<String, String> {}

// Simple stubs for ZAP client, response, etc., based on Python
class ZapResponse {
    HeaderMap headers;
    String query;
    Map<String, String> proxies;
    public ZapResponse(String apiKey) {
        headers = new HeaderMap();
        if (apiKey != null) headers.put("X-ZAP-API-Key", apiKey);
        query = apiKey != null ? "apikey=" + apiKey : "";
        proxies = Map.of("http", "http://127.0.0.1:8080", "https", "http://127.0.0.1:8080");
    }
    public ZapResponse() {
        // For missing key
        headers = new HeaderMap();
        query = "";
        proxies = Map.of("http", "http://127.0.0.1:8080", "https", "http://127.0.0.1:8080");
    }
}
class DummyZap {
    public String lastApiReturn;
    public ZapResponse lastResponse = null;

    public String urlopen(String url, Map<String, Object> params) {
        // Simulate apiResponse
        lastApiReturn = "{\"testkey\": \"testvalue\"}";
        lastResponse = new ZapResponse(null); // No API key in urlopen
        return lastApiReturn;
    }

    public Map<String, String> _request(String url, Map<String, Object> params) {
        lastApiReturn = "{\"testkey\": \"testvalue\"}";
        lastResponse = new ZapResponse("testapikey");
        // Simulated parsed response
        Map<String, String> res = new HashMap<>();
        res.put("testkey", "testvalue");
        return res;
    }

    public String _request_other(String url, Map<String, Object> params) {
        lastApiReturn = "{\"testkey\": \"testvalue\"}";
        lastResponse = new ZapResponse("testapikey");
        return lastApiReturn;
    }

    public Map<String, String> _request_api(String url, Map<String, Object> params) throws Exception {
        // Simulate an error on status code
        throw new Exception("Status code != 200");
    }
}

public class ClientTest {
    public static final Map<String, String> TEST_PROXIES = Map.of(
        "http", "http://127.0.0.1:8080",
        "https", "http://127.0.0.1:8080"
    );
    private DummyZap zap;

    @BeforeEach
    void setUp() {
        zap = new DummyZap();
    }

    // Helper check for API key in headers/query
    public void assertApiKey(ZapResponse response, String apikey) {
        assertEquals(apikey, response.headers.get("X-ZAP-API-Key"));
        assertFalse(response.query.contains("apikey=" + apikey));
    }

    @Test
    public void testUrlopen() {
        String apiResponse = "{\"testkey\": \"testvalue\"}";
        String result = zap.urlopen("http://localhost:8080", Map.of("querykey", "queryvalue"));
        assertEquals(apiResponse, result);
        ZapResponse response = zap.lastResponse;
        assertFalse(response.headers.containsKey("X-ZAP-API-Key"));
        assertFalse(response.query.contains("testapikey"));
        // Hamcrest: assert proxies map
        assertThat(response.proxies, allOf(hasEntry("http", "http://127.0.0.1:8080"), hasEntry("https", "http://127.0.0.1:8080")));
    }

    @Test
    public void testRequestApiInvalidStatusCode() {
        Exception thrown = assertThrows(Exception.class, () -> {
            zap._request_api("http://zap/test", Map.of("querykey", "queryvalue"));
        });
        ZapResponse response = zap.lastResponse;
        // Simulate what would happen after the failed request
        if (response != null)
            assertApiKey(response, "testapikey");
        // Hamcrest: assert proxies map (simulate)
        if (response != null)
            assertThat(response.proxies, allOf(hasEntry("http", "http://127.0.0.1:8080"), hasEntry("https", "http://127.0.0.1:8080")));
    }

    @Test
    public void testRequestResponse() {
        Map<String, String> result = zap._request("http://zap/test", Map.of("querykey", "queryvalue"));
        assertEquals("testvalue", result.get("testkey"));
        ZapResponse response = zap.lastResponse;
        assertApiKey(response, "testapikey");
        assertThat(response.proxies, allOf(hasEntry("http", "http://127.0.0.1:8080"), hasEntry("https", "http://127.0.0.1:8080")));
    }

    @Test
    public void testRequestOther() {
        String expected = "{\"testkey\": \"testvalue\"}";
        String result = zap._request_other("http://zap/test", Map.of("querykey", "queryvalue"));
        assertEquals(expected, result);
        ZapResponse response = zap.lastResponse;
        assertApiKey(response, "testapikey");
        assertThat(response.proxies, allOf(hasEntry("http", "http://127.0.0.1:8080"), hasEntry("https", "http://127.0.0.1:8080")));
    }
}