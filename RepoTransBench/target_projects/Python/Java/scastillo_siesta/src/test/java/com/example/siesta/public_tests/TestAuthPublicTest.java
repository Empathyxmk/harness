package com.example.siesta.public_tests;

import com.example.siesta.auth.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;

public class TestAuthPublicTest {

    static class DummyRequestPublic implements Auth.AuthMethod.RequestIFace {
        private final java.util.Map<String, String> headers = new java.util.HashMap<>();
        @Override
        public java.util.Map<String, String> getHeaders() { return headers; }
    }

    @Test
    void test_basic_auth() {
        BasicAuth a = new BasicAuth("alice", "wonderland");
        Map<String, String> hdrs = a.generateHeaders();
        assertTrue(hdrs.containsKey("Authorization"));
        assertTrue(hdrs.get("Authorization").startsWith("Basic "));
    }

    @Test
    void test_call_sets_headers() {
        BasicAuth a = new BasicAuth("alice", "wonderland");
        DummyRequestPublic req = new DummyRequestPublic();
        a.attach(req);
        assertTrue(req.getHeaders().containsKey("Authorization"));
    }

    @Test
    void test_repr() {
        BasicAuth ba = new BasicAuth("someone", "secret");
        String rep = ba.toString();
        assertTrue(rep.contains("BasicAuth"));
    }

    @Test
    void test_bearer_token() {
        BearerToken bt = new BearerToken("publictoken456");
        Map<String, String> hdrs = bt.generateHeaders();
        assertEquals("Bearer publictoken456", hdrs.get("Authorization"));
        DummyRequestPublic req = new DummyRequestPublic();
        bt.attach(req);
        assertTrue(req.getHeaders().containsKey("Authorization"));
    }

    @Test
    void test_repr_bearer() {
        BearerToken b = new BearerToken("pubtoken");
        assertTrue(b.toString().contains("BearerToken"));
    }

    @Test
    void test_api_key_header_only() {
        ApiKey ak = new ApiKey("pubkey", "pubval", true);
        Map<String, String> hdrs = ak.generateHeaders();
        assertTrue(hdrs.containsKey("pubkey"));
        DummyRequestPublic req = new DummyRequestPublic();
        ak.attach(req);
        assertTrue(req.getHeaders().containsKey("pubkey"));
    }

    @Test
    void test_api_key_in_query_not_supported() {
        ApiKey ak = new ApiKey("querykey", "queryval", false);
        Map<String, String> hdrs = ak.generateHeaders();
        assertEquals(0, hdrs.size());
    }

    @Test
    void test_repr_api_key() {
        ApiKey ak = new ApiKey("pubapi", "pubvalue", true);
        assertTrue(ak.toString().contains("ApiKey"));
    }
}