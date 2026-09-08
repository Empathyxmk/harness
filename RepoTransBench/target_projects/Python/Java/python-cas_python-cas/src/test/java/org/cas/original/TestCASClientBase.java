package org.cas.original;

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

class TestCASClientBase {

    @Test
    void testLoginUrlHelper() {
        CASClientBase client = new CASClientBase(
                false, null,
                "http://www.example.com/cas/",
                "http://testserver/"
        );
        String actual = client.getLoginUrl();
        String expected = "http://www.example.com/cas/login?service=http%3A%2F%2Ftestserver%2F";
        assertEquals(expected, actual);
    }

    @Test
    void testLoginUrlHelperWithExtraParams() {
        Map<String, String> params = new HashMap<>();
        params.put("test", "1234");
        CASClientBase client = new CASClientBase(
                false, params,
                "http://www.example.com/cas/",
                "http://testserver/"
        );
        String actual = client.getLoginUrl();
        assertTrue(actual.contains("service=http%3A%2F%2Ftestserver%2F"));
        assertTrue(actual.contains("test=1234"));
    }

    @Test
    void testLoginUrlHelperWithRenew() {
        CASClientBase client = new CASClientBase(
                true, null,
                "http://www.example.com/cas/",
                "http://testserver/"
        );
        String actual = client.getLoginUrl();
        assertTrue(actual.contains("service=http%3A%2F%2Ftestserver%2F"));
        assertTrue(actual.contains("renew=true"));
    }

    @Test
    void testLogoutUrl() {
        CASClient client = new CASClient("3", "http://www.example.com/cas/");
        String actual = client.getLogoutUrl();
        String expected = "http://www.example.com/cas/logout";
        assertEquals(expected, actual);
    }
}