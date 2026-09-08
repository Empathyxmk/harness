package com.example.siesta.original;

import com.example.siesta.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestSiestaAPITest {

    @Test
    void test_foo_not_supported_print() {
        Util.foo_not_supported();
    }

    @Test
    void test_api_init_and_attr() {
        API api = new API("http://api.com");
        Resource resource = api.getResource("books");
        assertNotNull(resource);
        assertTrue(api.resources.containsKey("/books"));
        assertEquals("/books", resource.uri);
        assertEquals(api, resource.api);
        assertEquals("<API http://api.com>", api.toString());
        assertTrue(resource.toString().startsWith("<Resource /books"));
    }
}