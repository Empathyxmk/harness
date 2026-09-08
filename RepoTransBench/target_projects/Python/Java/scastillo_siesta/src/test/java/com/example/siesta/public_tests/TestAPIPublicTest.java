package com.example.siesta.public_tests;

import com.example.siesta.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestAPIPublicTest {
    @Test
    void test_api_init_repr() {
        API api = new API("http://newuri", "y");
        assertEquals("http://newuri", api.base_url);
        assertEquals("y", api.auth);
        String repr = api.toString();
        assertTrue(repr.contains("http://newuri"));
    }

    @Test
    void test_api_getattr() {
        API api = new API("http://newuri");
        Resource res = api.getResource("bar");
        assertNotNull(res);
        assertTrue(api.resources.containsKey("/bar"));
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