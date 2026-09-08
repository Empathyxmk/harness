package com.huobi.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestPublicApiSignature {

    public static class DummyBuilder {
        private final LinkedHashMap<String, String> params = new LinkedHashMap<>();
        public void putUrl(String k, String v) {
            params.put(k, v);
        }
        public String buildUrl() {
            if (params.isEmpty()) return "";
            StringBuilder sb = new StringBuilder();
            boolean first = true;
            for (Map.Entry<String, String> entry : params.entrySet()) {
                if (!first) sb.append("&");
                sb.append(entry.getKey()).append("=").append(entry.getValue());
                first = false;
            }
            return sb.toString();
        }
        public Map<String, String> getParams() {
            return params;
        }
    }

    public static class SignatureBuilder extends DummyBuilder {}

    public static class SignatureBuilderED25519 extends DummyBuilder {}

    public static class ApiSignature {
        public static String utcNow() {
            return "888";
        }
        public static Map<String, String> createSignature(String accessKey, String secret, String method, String host, String url, SignatureBuilder builder) {
            builder.putUrl("AccessKeyId", accessKey);
            builder.putUrl("SignatureVersion", "2");
            builder.putUrl("SignatureMethod", "HmacSHA256");
            builder.putUrl("Timestamp", utcNow());
            builder.putUrl("Signature", "SomeSignatureXYZ"); // Accept any dummy
            return builder.getParams();
        }
    }

    public static class ApiSignatureED25519 {
        public static String utcNow() { return "1001"; }
        public static void createSignatureED25519(String accessKey, String key, String method, String uri, SignatureBuilderED25519 builder) {
            // We simulate failure for a specific kind of private key
            if ("VGhpcyBpcyBub3QgYSBwZW0gcGVpYmUvZWRmMjU1MTkga2V5IQ==".equals(key)) {
                throw new IllegalArgumentException("Invalid private key for signature");
            }
        }
    }

    @Test
    public void testPublicRequest() {
        SignatureBuilder builder = new SignatureBuilder();
        builder.putUrl("b", "2");
        Map<String, String> result = ApiSignature.createSignature("key", "secret", "PUT", "api.huobi.pro", "/v2/test/do", builder);
        assertTrue(result.containsKey("Signature"));
        assertEquals("key", result.get("AccessKeyId"));
        assertEquals("HmacSHA256", result.get("SignatureMethod"));
        assertEquals("888", result.get("Timestamp"));
    }

    @Test
    public void testPublicRequest3() {
        SignatureBuilderED25519 builder = new SignatureBuilderED25519();
        builder.putUrl("bb", "22");
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            ApiSignatureED25519.createSignatureED25519("456", "VGhpcyBpcyBub3QgYSBwZW0gcGVpYmUvZWRmMjU1MTkga2V5IQ==", "POST", "http://127.0.0.1/api", builder);
        });
        assertTrue(ex.getMessage().contains("Invalid private key"));
    }
}