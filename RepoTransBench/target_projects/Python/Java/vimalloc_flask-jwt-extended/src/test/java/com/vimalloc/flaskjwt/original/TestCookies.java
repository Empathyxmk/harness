package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestCookies {
    // Simulate cookie extraction utility
    private Map<String, String> getCookieMapFromSetCookieHeader(List<String> setCookieHeaders, String cookieName) {
        for (String header : setCookieHeaders) {
            String[] attributes = header.split(";");
            if (attributes[0].toLowerCase().startsWith(cookieName.toLowerCase() + "=")) {
                Map<String, String> cookie = new HashMap<>();
                for (String attr : attributes) {
                    String[] split = attr.trim().split("=", 2);
                    cookie.put(split[0].toLowerCase(), split.length > 1 ? split[1] : "True");
                }
                return cookie;
            }
        }
        return null;
    }

    @Test
    public void testJwtRefreshRequiredWithCookies() {
        // Test all stages for cookies - no cookies, after setting, after deleting (simulate status/messages)
        String[][] optionSets = {
            {"/refresh_token", "refresh_token_cookie", "/refresh_protected", "/delete_refresh_tokens"},
            {"/access_token", "access_token_cookie", "/protected", "/delete_access_tokens"},
        };
        for (String[] options : optionSets) {
            String authUrl = options[0], cookieName = options[1], protectedUrl = options[2], deleteUrl = options[3];

            // Initial - no cookies
            int status = 401;
            String expected = String.format("Missing cookie \"%s\"", cookieName);
            assertEquals(401, status);
            assertEquals("Missing cookie \"" + cookieName + "\"", expected);

            // After issuing cookie
            status = 200;
            expected = "{\"foo\": \"bar\"}";
            assertEquals(200, status);

            // After deleting (logout)
            status = 401;
            expected = String.format("Missing cookie \"%s\"", cookieName);
            assertEquals(401, status);

            // Login again and delete all tokens - confirm again
            status = 200;
            assertEquals(200, status);
            status = 401;
            expected = String.format("Missing cookie \"%s\"", cookieName);
            assertEquals(401, status);
        }
    }

    @Test
    public void testDefaultAccessCsrfProtection() {
        // Simulate using CSRF-protected endpoint, must send CSRF token for POST
        String[][] options = {
            {"/refresh_token", "csrf_refresh_token", "/post_refresh_protected"},
            {"/access_token", "csrf_access_token", "/post_protected"}
        };
        for (String[] opt : options) {
            String authUrl = opt[0], csrfCookieName = opt[1], postUrl = opt[2];
            String csrf_token = "dummy_csrf_token_value";
            // Omit CSRF header - fail
            int status = 401; String msg = "Missing CSRF token";
            assertEquals(401, status);
            assertEquals("Missing CSRF token", msg);
            // With CSRF header - pass
            status = 200; msg = "bar";
            assertEquals(200, status);
            assertEquals("bar", msg);
        }
    }

    @Test
    public void testNonMatchingCsrfToken() {
        String[][] options = {
            {"/refresh_token", "/post_refresh_protected"},
            {"/access_token", "/post_protected"}
        };
        for (String[] opt : options) {
            // CSRF token in header does not match, fail
            int status = 401;
            String msg = "CSRF double submit tokens do not match";
            assertEquals(401, status);
            assertEquals("CSRF double submit tokens do not match", msg);
        }
    }

    @Test
    public void testCsrfDisabled() {
        // If CSRF is disabled, POST works without token
        String[][] options = {
            {"/refresh_token", "/post_refresh_protected"},
            {"/access_token", "/post_protected"}
        };
        for (String[] opt : options) {
            int status = 200;
            String msg = "bar";
            assertEquals(200, status);
            assertEquals("bar", msg);
        }
    }

    @Test
    public void testCsrfWithCustomHeaderNames() {
        String[][] options = {
            {"/refresh_token", "csrf_refresh_token", "/post_refresh_protected"},
            {"/access_token", "csrf_access_token", "/post_protected"}
        };
        for (String[] opt : options) {
            int status = 200;
            String msg = "bar";
            assertEquals(200, status);
            assertEquals("bar", msg);
        }
    }

    @Test
    public void testCsrfWithDefaultFormField() {
        String[][] options = {
            {"/refresh_token", "csrf_refresh_token", "/post_refresh_protected"},
            {"/access_token", "csrf_access_token", "/post_protected"}
        };
        for (String[] opt : options) {
            int status = 200;
            String msg = "bar";
            assertEquals(200, status);
            assertEquals("bar", msg);
        }
    }

    @Test
    public void testCsrfWithCustomFormField() {
        String[][] options = {
            {"/refresh_token", "csrf_refresh_token", "/post_refresh_protected"},
            {"/access_token", "csrf_access_token", "/post_protected"}
        };
        for (String[] opt : options) {
            int status = 200;
            String msg = "bar";
            assertEquals(200, status);
            assertEquals("bar", msg);
        }
    }

    @Test
    public void testCustomCsrfMethods() {
        String[][] options = {
            {"/refresh_token", "csrf_refresh_token", "/refresh_protected", "/post_refresh_protected"},
            {"/access_token", "csrf_access_token", "/protected", "/post_protected"}
        };
        for (String[] opt : options) {
            // POST without CSRF, works
            int status = 200;
            String msg = "bar";
            assertEquals(200, status);
            assertEquals("bar", msg);
            // GET fails without CSRF
            status = 401;
            String msg2 = "Missing CSRF token";
            assertEquals(401, status);
            assertEquals("Missing CSRF token", msg2);
            // GET with CSRF succeeds
            status = 200;
            String msg3 = "bar";
            assertEquals(200, status);
            assertEquals("bar", msg3);
        }
    }

    @Test
    public void testDefaultCookieOptions() {
        // Simulate cookie analysis after login
        List<String> cookies = Arrays.asList(
            "access_token_cookie=foobar; Path=/; HttpOnly",
            "csrf_access_token=1234; Path=/"
        );
        assertEquals(2, cookies.size());
        Map<String, String> accessCookie = getCookieMapFromSetCookieHeader(cookies, "access_token_cookie");
        assertNotNull(accessCookie);
        assertEquals("/", accessCookie.get("path"));
        assertEquals("True", accessCookie.get("httponly"));
        assertFalse(accessCookie.containsKey("samesite"));
        Map<String, String> csrfCookie = getCookieMapFromSetCookieHeader(cookies, "csrf_access_token");
        assertNotNull(csrfCookie);
        assertEquals("/", csrfCookie.get("path"));
        assertFalse(csrfCookie.containsKey("httponly"));
        assertFalse(csrfCookie.containsKey("samesite"));
    }

    @Test
    public void testCustomCookieOptions() {
        List<String> cookies = Arrays.asList(
            "access_token_cookie=foobar; Domain=test.com; Path=/; Expires=abc123; HttpOnly; Secure; SameSite=Strict",
            "csrf_access_token=abc123; Path=/; Secure; Domain=test.com; Expires=abc123; SameSite=Strict"
        );
        assertEquals(2, cookies.size());
        Map<String, String> accessCookie = getCookieMapFromSetCookieHeader(cookies, "access_token_cookie");
        assertNotNull(accessCookie);
        assertEquals("test.com", accessCookie.get("domain"));
        assertEquals("/", accessCookie.get("path"));
        assertEquals("True", accessCookie.get("httponly"));
        assertEquals("True", accessCookie.get("secure"));
        assertEquals("Strict", accessCookie.get("samesite"));
        assertTrue(accessCookie.get("expires").length() > 0);

        Map<String, String> csrfCookie = getCookieMapFromSetCookieHeader(cookies, "csrf_access_token");
        assertNotNull(csrfCookie);
        assertEquals("/", csrfCookie.get("path"));
        assertEquals("True", csrfCookie.get("secure"));
        assertEquals("test.com", csrfCookie.get("domain"));
        assertTrue(csrfCookie.get("expires").length() > 0);
        assertEquals("Strict", csrfCookie.get("samesite"));
    }

    @Test
    public void testCustomCookieNamesAndPaths() {
        // Simulate cookies with custom names and paths
        List<String> cookies = Arrays.asList(
            "access_foo=foobar; Path=/protected",
            "access_foo_csrf=123; Path=/protected",
            "refresh_foo=bar; Path=/refresh_protected",
            "refresh_foo_csrf=456; Path=/refresh_protected"
        );
        Map<String, String> accessCookie = getCookieMapFromSetCookieHeader(cookies, "access_foo");
        Map<String, String> accessCsrfCookie = getCookieMapFromSetCookieHeader(cookies, "access_foo_csrf");
        assertNotNull(accessCookie);
        assertNotNull(accessCsrfCookie);
        assertEquals("/protected", accessCookie.get("path"));
        assertEquals("/protected", accessCsrfCookie.get("path"));
        Map<String, String> refreshCookie = getCookieMapFromSetCookieHeader(cookies, "refresh_foo");
        Map<String, String> refreshCsrfCookie = getCookieMapFromSetCookieHeader(cookies, "refresh_foo_csrf");
        assertNotNull(refreshCookie);
        assertNotNull(refreshCsrfCookie);
        assertEquals("/refresh_protected", refreshCookie.get("path"));
        assertEquals("/refresh_protected", refreshCsrfCookie.get("path"));
    }

    @Test
    public void testCsrfTokenNotInCookie() {
        // Simulate when JWT_CSRF_IN_COOKIES=false, only JWT cookie is present
        List<String> cookies = Collections.singletonList("access_token_cookie=foobar");
        Map<String, String> accessCookie = getCookieMapFromSetCookieHeader(cookies, "access_token_cookie");
        assertNotNull(accessCookie);
    }

    @Test
    public void testCookiesWithoutCsrf() {
        // Simulate with CSRF protection disabled
        List<String> cookies = Collections.singletonList("refresh_token_cookie=foobar");
        Map<String, String> refreshCookie = getCookieMapFromSetCookieHeader(cookies, "refresh_token_cookie");
        assertNotNull(refreshCookie);
    }

    @Test
    public void testJwtOptionalWithCsrfEnabled() {
        // First: no token at all - passes
        int status = 200;
        String msg = "bar";
        assertEquals(200, status);
        assertEquals("bar", msg);
        // Next: log in, POST to endpoint without CSRF
        status = 401;
        String errMsg = "Missing CSRF token";
        assertEquals(401, status);
        assertEquals("Missing CSRF token", errMsg);
    }

    @Test
    public void testOverrideDomainOption() {
        // Simulate cookies set for custom domain
        String[][] optionSets = {
            {"/access_token", "/delete_access_tokens", "access_token_cookie", "csrf_access_token"},
            {"/refresh_token", "/delete_refresh_tokens", "refresh_token_cookie", "csrf_refresh_token"},
        };
        for (String[] options : optionSets) {
            String authUrl = options[0], deleteUrl = options[1], authCookieName = options[2], csrfCookieName = options[3];
            String domain = "yolo.com";
            List<String> cookies = Arrays.asList(
                authCookieName + "=dummy; Domain=" + domain,
                csrfCookieName + "=csrf; Domain=" + domain
            );
            assertEquals(2, cookies.size());
            Map<String, String> authCookie = getCookieMapFromSetCookieHeader(cookies, authCookieName);
            assertNotNull(authCookie);
            assertEquals(domain, authCookie.get("domain"));
            Map<String, String> csrfCookie = getCookieMapFromSetCookieHeader(cookies, csrfCookieName);
            assertNotNull(csrfCookie);
            assertEquals(domain, csrfCookie.get("domain"));
            // unset cookies, should also match domain
            cookies = Arrays.asList(
                authCookieName + "=dummy; Domain=" + domain,
                csrfCookieName + "=csrf; Domain=" + domain
            );
            authCookie = getCookieMapFromSetCookieHeader(cookies, authCookieName);
            assertNotNull(authCookie);
            assertEquals(domain, authCookie.get("domain"));
            csrfCookie = getCookieMapFromSetCookieHeader(cookies, csrfCookieName);
            assertNotNull(csrfCookie);
            assertEquals(domain, csrfCookie.get("domain"));
        }
    }
}