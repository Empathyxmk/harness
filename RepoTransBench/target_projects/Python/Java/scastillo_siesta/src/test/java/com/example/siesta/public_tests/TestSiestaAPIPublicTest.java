package com.example.siesta.public_tests;

import com.example.siesta.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestSiestaAPIPublicTest {

    @Test
    void test_foo_not_supported_print() {
        Util.foo_not_supported();
    }

    @Test
    void test_api_init_and_attr() {
        API api = new API("http://publicapi.org");
        Resource resource = api.getResource("users");
        assertNotNull(resource);
        assertTrue(api.resources.containsKey("/users"));
        assertEquals("/users", resource.uri);
        assertEquals(api, resource.api);
        assertEquals("<API http://publicapi.org>", api.toString());
        assertTrue(resource.toString().startsWith("<Resource /users"));
    }
}