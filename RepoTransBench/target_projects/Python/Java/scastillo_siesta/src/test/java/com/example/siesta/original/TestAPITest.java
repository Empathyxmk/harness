package com.example.siesta.original;

import com.example.siesta.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestAPITest {
    @Test
    void test_api_init_repr() {
        API api = new API("http://uri", "x");
        assertEquals("http://uri", api.base_url);
        assertEquals("x", api.auth);
        String repr = api.toString();
        assertTrue(repr.contains("http://uri"));
    }

    @Test
    void test_api_getattr() {
        API api = new API("http://uri");
        Resource res = api.getResource("foo");
        assertNotNull(res);
        assertTrue(api.resources.containsKey("/foo"));
    }

    @Test
    void test_foo_not_supported() {
        try {
            Util.foo_not_supported(); // Should print, not fail
        } catch (Exception ex) {
            fail("foo_not_supported should not throw");
        }
    }
}