package com.typeerror.secure.public_;

import com.typeerror.secure.secure.*;
import com.typeerror.secure.headers.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class TestSecurePublic {

    static class PublicMockResponse implements HeadersProtocol, SetHeaderProtocol {
        public Map<String, String> headers = new HashMap<>();
        @Override public Map<String, String> getHeaders() { return headers; }
        @Override public void setHeader(String key, String value) { headers.put(key, value); }
    }
    static class PublicMockResponseWithSetHeader implements HeadersProtocol, SetHeaderProtocol {
        public Map<String, String> headers = new HashMap<>();
        public Map<String, String> storage = new HashMap<>();
        @Override public Map<String, String> getHeaders() { return headers; }
        @Override public void setHeader(String key, String value) { storage.put(key, value); }
    }

    private Secure secure;

    @BeforeEach
    public void setUp() {
        CustomHeader ch1 = new CustomHeader("X-Public-Header-1", "PubValue1");
        CustomHeader ch2 = new CustomHeader("X-Public-Header-2", "PubValue2");
        secure = new Secure.Builder().custom(Arrays.asList(ch1, ch2)).build();
        // Simulate python field: precompute headers map
        Map<String, String> headersMap = new LinkedHashMap<>();
        for (Object header : secure.getHeadersList()) {
            if (header instanceof BaseHeader) {
                BaseHeader bh = (BaseHeader) header;
                headersMap.put(bh.getHeaderName(), bh.getHeaderValue());
            }
            if (header instanceof CustomHeader) {
                CustomHeader ch = (CustomHeader) header;
                headersMap.put(ch.getHeaderName(), ch.getHeaderValue());
            }
        }
        secure.setHeadersMap(headersMap);
    }

    @Test
    public void testWithPublicHeaders() {
        Secure secureHeaders = new Secure.Builder()
                .csp(new ContentSecurityPolicy().defaultSrc("'self'").imgSrc("'public'"))
                .server(new Server().set("PublicServer"))
                .custom(Arrays.asList(new CustomHeader("X-Test-Key", "TestVal")))
                .build();
        PublicMockResponse response = new PublicMockResponse();
        secureHeaders.setHeaders(response);

        Map<String, String> resHdrs = response.headers;
        assertTrue(resHdrs.containsKey("Content-Security-Policy"));
        assertEquals("default-src 'self'; img-src 'public'", resHdrs.get("Content-Security-Policy"));
        assertTrue(resHdrs.containsKey("Server"));
        assertEquals("PublicServer", resHdrs.get("Server"));
        assertTrue(resHdrs.containsKey("X-Test-Key"));
        assertEquals("TestVal", resHdrs.get("X-Test-Key"));
        assertFalse(resHdrs.containsKey("Strict-Transport-Security"));
    }

    @Test
    public void testFromPresetBasicPublic() {
        Secure secureHeaders = Secure.fromPreset(Preset.BASIC);
        PublicMockResponse response = new PublicMockResponse();
        secureHeaders.setHeaders(response);

        Map<String, String> resHdrs = response.headers;
        assertTrue(resHdrs.containsKey("Cache-Control"));
        assertEquals("no-store", resHdrs.get("Cache-Control"));

        assertTrue(resHdrs.containsKey("Referrer-Policy"));
        assertEquals("strict-origin-when-cross-origin", resHdrs.get("Referrer-Policy"));

        assertTrue(resHdrs.containsKey("Server"));
        assertEquals("", resHdrs.get("Server"));

        assertTrue(resHdrs.containsKey("Strict-Transport-Security"));
        assertEquals("max-age=31536000", resHdrs.get("Strict-Transport-Security"));

        assertTrue(resHdrs.containsKey("X-Content-Type-Options"));
        assertEquals("nosniff", resHdrs.get("X-Content-Type-Options"));

        assertTrue(resHdrs.containsKey("X-Frame-Options"));
        assertEquals("SAMEORIGIN", resHdrs.get("X-Frame-Options"));

        assertFalse(resHdrs.containsKey("Content-Security-Policy"));
        assertFalse(resHdrs.containsKey("Permissions-Policy"));
        assertFalse(resHdrs.containsKey("Cross-Origin-Opener-Policy"));
    }

    @Test
    public void testFromPresetStrictPublic() {
        Secure secureHeaders = Secure.fromPreset(Preset.STRICT);
        PublicMockResponse response = new PublicMockResponse();
        secureHeaders.setHeaders(response);

        Map<String, String> resHdrs = response.headers;
        assertTrue(resHdrs.containsKey("Cache-Control"));
        assertEquals("no-store", resHdrs.get("Cache-Control"));

        assertTrue(resHdrs.containsKey("Content-Security-Policy"));
        assertEquals("default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'", resHdrs.get("Content-Security-Policy"));

        assertTrue(resHdrs.containsKey("Cross-Origin-Embedder-Policy"));
        assertEquals("require-corp", resHdrs.get("Cross-Origin-Embedder-Policy"));

        assertTrue(resHdrs.containsKey("Cross-Origin-Opener-Policy"));
        assertEquals("same-origin", resHdrs.get("Cross-Origin-Opener-Policy"));

        assertTrue(resHdrs.containsKey("Permissions-Policy"));
        assertEquals("geolocation=(), microphone=(), camera=()", resHdrs.get("Permissions-Policy"));

        assertTrue(resHdrs.containsKey("Referrer-Policy"));
        assertEquals("no-referrer", resHdrs.get("Referrer-Policy"));

        assertTrue(resHdrs.containsKey("Server"));
        assertEquals("", resHdrs.get("Server"));

        assertTrue(resHdrs.containsKey("Strict-Transport-Security"));
        assertEquals("max-age=63072000; includeSubDomains; preload", resHdrs.get("Strict-Transport-Security"));

        assertTrue(resHdrs.containsKey("X-Content-Type-Options"));
        assertEquals("nosniff", resHdrs.get("X-Content-Type-Options"));

        assertTrue(resHdrs.containsKey("X-Frame-Options"));
        assertEquals("DENY", resHdrs.get("X-Frame-Options"));
    }

    @Test
    public void testCustomHeadersPublic() {
        Server customServer = new Server().set("AnotherServer");
        ContentSecurityPolicy customCsp = new ContentSecurityPolicy().defaultSrc("'public'").styleSrc("'test'");
        Secure secureHeaders = new Secure.Builder()
                .server(customServer)
                .csp(customCsp)
                .build();

        PublicMockResponse response = new PublicMockResponse();
        secureHeaders.setHeaders(response);

        Map<String, String> resHdrs = response.headers;
        assertTrue(resHdrs.containsKey("Server"));
        assertEquals("AnotherServer", resHdrs.get("Server"));

        assertTrue(resHdrs.containsKey("Content-Security-Policy"));
        assertEquals("default-src 'public'; style-src 'test'", resHdrs.get("Content-Security-Policy"));
    }
}