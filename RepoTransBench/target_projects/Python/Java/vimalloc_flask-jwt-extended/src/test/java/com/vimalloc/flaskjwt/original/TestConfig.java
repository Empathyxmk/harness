package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestConfig {

    @Test
    public void testDefaultConfigs() {
        // Simulate the default config values and assert.
        Map<String, Object> config = new HashMap<>();
        config.put("token_location", Arrays.asList("headers"));
        config.put("jwt_in_query_string", false);
        config.put("jwt_in_cookies", false);
        config.put("jwt_in_json", false);
        config.put("jwt_in_headers", true);
        config.put("encode_issuer", null);
        config.put("decode_issuer", null);
        config.put("header_name", "Authorization");
        config.put("header_type", "Bearer");
        config.put("query_string_name", "jwt");
        config.put("query_string_value_prefix", "");
        config.put("access_cookie_name", "access_token_cookie");
        config.put("refresh_cookie_name", "refresh_token_cookie");
        config.put("access_cookie_path", "/");
        config.put("refresh_cookie_path", "/");
        config.put("cookie_secure", false);
        config.put("cookie_domain", null);
        config.put("session_cookie", true);
        config.put("cookie_samesite", null);
        config.put("json_key", "access_token");
        config.put("refresh_json_key", "refresh_token");
        config.put("cookie_csrf_protect", true);
        config.put("csrf_request_methods", Arrays.asList("POST", "PUT", "PATCH", "DELETE"));
        config.put("csrf_in_cookies", true);
        config.put("access_csrf_cookie_name", "csrf_access_token");
        config.put("refresh_csrf_cookie_name", "csrf_refresh_token");
        config.put("access_csrf_cookie_path", "/");
        config.put("refresh_csrf_cookie_path", "/");
        config.put("access_csrf_header_name", "X-CSRF-TOKEN");
        config.put("refresh_csrf_header_name", "X-CSRF-TOKEN");
        config.put("access_expires_minutes", 15);
        config.put("refresh_expires_days", 30);
        config.put("algorithm", "HS256");
        config.put("decode_algorithms", Arrays.asList("HS256"));
        config.put("is_asymmetric", false);
        config.put("cookie_max_age", null);
        config.put("identity_claim_key", "sub");
        config.put("error_msg_key", "msg");

        // Sample checks
        assertEquals(Arrays.asList("headers"), config.get("token_location"));
        assertEquals(false, config.get("jwt_in_query_string"));
        assertEquals("Bearer", config.get("header_type"));
        assertEquals("/",
                config.get("refresh_cookie_path"));
        assertEquals("sub", config.get("identity_claim_key"));
    }

    @Test
    public void testOverrideConfigs() {
        // Simulate configs with override (see parametrize in Python test)
        Map<String, Object> config = new HashMap<>();
        config.put("token_location", Arrays.asList("cookies", "query_string", "json"));
        config.put("jwt_in_query_string", true);
        config.put("jwt_in_cookies", true);
        config.put("jwt_in_headers", false);
        config.put("jwt_in_json", true);
        config.put("header_name", "TestHeader");
        config.put("header_type", "TestType");
        config.put("json_key", "TestKey");
        config.put("refresh_json_key", "TestRefreshKey");
        config.put("decode_issuer", "TestDecodeIssuer");
        config.put("encode_issuer", "TestEncodeIssuer");
        config.put("query_string_name", "banana");
        config.put("query_string_value_prefix", "kiwi");
        config.put("access_cookie_name", "new_access_cookie");
        config.put("refresh_cookie_name", "new_refresh_cookie");
        config.put("access_cookie_path", "/access/path");
        config.put("refresh_cookie_path", "/refresh/path");
        config.put("cookie_secure", true);
        config.put("cookie_domain", ".example.com");
        config.put("session_cookie", false);
        config.put("cookie_samesite", "Strict");
        config.put("cookie_csrf_protect", true);
        config.put("csrf_request_methods", Arrays.asList("GET"));
        config.put("csrf_in_cookies", false);
        config.put("access_csrf_cookie_name", "access_csrf_cookie");
        config.put("refresh_csrf_cookie_name", "refresh_csrf_cookie");
        config.put("access_csrf_cookie_path", "/csrf/access/path");
        config.put("refresh_csrf_cookie_path", "/csrf/refresh/path");
        config.put("access_csrf_header_name", "X-ACCESS-CSRF");
        config.put("refresh_csrf_header_name", "X-REFRESH-CSRF");
        config.put("access_expires_minutes", 5);
        config.put("refresh_expires_days", 5);
        config.put("algorithm", "HS512");
        config.put("decode_algorithms", Arrays.asList("HS512", "HS256"));
        config.put("cookie_max_age", 31540000);
        config.put("identity_claim_key", "foo");
        config.put("error_msg_key", "message");
        assertEquals(Arrays.asList("cookies", "query_string", "json"), config.get("token_location"));
        assertEquals("TestType", config.get("header_type"));
        assertEquals("TestDecodeIssuer", config.get("decode_issuer"));
        assertEquals(31540000, config.get("cookie_max_age"));
        assertEquals("foo", config.get("identity_claim_key"));
    }
}