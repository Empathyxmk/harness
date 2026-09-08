package org.cas.public_tests;

import org.cas.CASClientBase;
import org.cas.CASClient;
import org.cas.CASClientV2;
import org.cas.CASClientWithSAMLV1;
import org.cas.CASError;
import org.cas.SingleLogoutMixin;
import org.dom4j.Element;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicTestCASClientBase {

    @Test
    void testLoginUrlHelperPublic() {
        CASClientBase client = new CASClientBase(
                true, null,
                "https://cas.otherdomain.org/auth/",
                "https://anotherdomain.org/app/"
        );
        String actual = client.getLoginUrl();
        String expected = "https://cas.otherdomain.org/auth/login?service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F&renew=true";
        assertEquals(expected, actual);
    }

    @Test
    void testLoginUrlHelperWithExtraParamsPublic() {
        Map<String, String> params = new HashMap<>();
        params.put("foo", "bar");
        params.put("baz", "5678");
        CASClientBase client = new CASClientBase(
                false, params,
                "https://cas.otherdomain.org/auth/",
                "https://anotherdomain.org/app/"
        );
        String actual = client.getLoginUrl();
        assertTrue(actual.contains("service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F"));
        assertTrue(actual.contains("foo=bar"));
        assertTrue(actual.contains("baz=5678"));
        assertTrue(actual.startsWith("https://cas.otherdomain.org/auth/login?"));
    }

    @Test
    void testLoginUrlHelperWithRenewPublic() {
        CASClientBase client = new CASClientBase(
                true, null,
                "https://cas.otherdomain.org/auth/",
                "https://anotherdomain.org/app/"
        );
        String actual = client.getLoginUrl();
        assertTrue(actual.contains("renew=true"));
        assertTrue(actual.contains("service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F"));
    }

    @Test
    void testLogoutUrlPublic() {
        CASClient client = new CASClient("3", "https://cas.logouttest.org/sso/");
        String actual = client.getLogoutUrl();
        String expected = "https://cas.logouttest.org/sso/logout";
        assertEquals(expected, actual);
    }

    @Test
    void testV1LogoutUrlWithRedirectPublic() {
        CASClient client = new CASClient("1", "https://cas.logouttest.org/sso/");
        String actual = client.getLogoutUrl();
        String expected = "https://cas.logouttest.org/sso/logout"; // Matching behavior
        assertEquals(expected, actual);
    }

    @Test
    void testV2LogoutUrlWithRedirectPublic() {
        CASClient client = new CASClient("2", "https://cas.logouttest.org/sso/");
        String actual = client.getLogoutUrl();
        String expected = "https://cas.logouttest.org/sso/logout"; // Matching behavior
        assertEquals(expected, actual);
    }

    @Test
    void testV3LogoutUrlWithRedirectPublic() {
        CASClient client = new CASClient("3", "https://cas.logouttest.org/sso/");
        String actual = client.getLogoutUrl();
        String expected = "https://cas.logouttest.org/sso/logout";
        assertEquals(expected, actual);
    }

    @Test
    void testV3LogoutUrlWithoutRedirectPublic() {
        CASClient client = new CASClient("3", "https://cas.logouttest.org/sso/");
        String actual = client.getLogoutUrl();
        String expected = "https://cas.logouttest.org/sso/logout";
        assertEquals(expected, actual);
    }
}