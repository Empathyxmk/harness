package com.example.siesta.original;

import com.example.siesta.auth.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;

public class TestAuthTest {

    static class DummyRequestImpl implements Auth.AuthMethod.RequestIFace {
        private final java.util.Map<String, String> headers = new java.util.HashMap<>();
        @Override
        public java.util.Map<String, String> getHeaders() { return headers; }
    }

    @Test
    void test_basic_auth() {
        BasicAuth a = new BasicAuth("foo", "bar");
        Map<String, String> hdrs = a.generateHeaders();
        assertTrue(hdrs.containsKey("Authorization"));
        assertTrue(hdrs.get("Authorization").startsWith("Basic "));
    }

    @Test
    void test_call_sets_headers() {
        BasicAuth a = new BasicAuth("foo", "bar");
        DummyRequestImpl req = new DummyRequestImpl();
        a.attach(req);
        assertTrue(req.getHeaders().containsKey("Authorization"));
    }

    @Test
    void test_repr() {
        BasicAuth ba = new BasicAuth("username", "pw");
        String rep = ba.toString();
        assertTrue(rep.contains("BasicAuth"));
    }

    @Test
    void test_bearer_token() {
        BearerToken bt = new BearerToken("tok123");
        Map<String, String> hdrs = bt.generateHeaders();
        assertEquals("Bearer tok123", hdrs.get("Authorization"));
        DummyRequestImpl req = new DummyRequestImpl();
        bt.attach(req);
        assertTrue(req.getHeaders().containsKey("Authorization"));
    }

    @Test
    void test_repr_bearer() {
        BearerToken b = new BearerToken("tk");
        assertTrue(b.toString().contains("BearerToken"));
    }

    @Test
    void test_api_key_header_only() {
        ApiKey ak = new ApiKey("mykey", "myval", true);
        Map<String, String> hdrs = ak.generateHeaders();
        assertTrue(hdrs.containsKey("mykey"));
        DummyRequestImpl req = new DummyRequestImpl();
        ak.attach(req);
        assertTrue(req.getHeaders().containsKey("mykey"));
    }

    @Test
    void test_api_key_in_query_not_supported() {
        ApiKey ak = new ApiKey("qkey", "qval", false);
        Map<String, String> hdrs = ak.generateHeaders();
        assertEquals(0, hdrs.size());
    }

    @Test
    void test_repr_api_key() {
        ApiKey ak = new ApiKey("api", "value", true);
        assertTrue(ak.toString().contains("ApiKey"));
    }
}