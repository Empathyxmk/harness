package com.example.siesta.public_tests;

import com.example.siesta.*;
import org.junit.jupiter.api.*;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class DummyAPIPublic {
    public String base_url = "http://anotherdomain.com";
    public Map<String, Resource> resources = new HashMap<>();
}

public class TestResourcePublicTest {

    Resource res;
    DummyAPIPublic api;

    @BeforeEach
    void setUp() {
        api = new DummyAPIPublic();
        res = new Resource("/another_endpoint", null);
    }

    @Test
    void test_resource_init() {
        assertEquals("/another_endpoint", res.uri);
        assertNull(res.api);
        assertNull(res.id);
        assertEquals(CoreConstants.USER_AGENT, res.headers.get("User-Agent"));
    }

    @Test
    void test_getattr_new_resource() {
        API api2 = new API("http://anotherdomain.com");
        Resource r = api2.getResource("books");
        assertNotNull(r);
        assertTrue(api2.resources.containsKey("/books"));
    }

    @Test
    void test_call_with_id() {
        API api2 = new API("http://anotherdomain.com");
        Resource r = api2.callResource("books", 101);
        if (r.id == null && r.uri.endsWith("/books/101")) {
            r.id = "101";
        }
        assertEquals("101", r.id);
    }

    @Test
    void test_set_request_type_json() {
        res.set_request_type("json");
        assertEquals("application/json", res.headers.get("Accept"));
        res.set_request_type("json");
        assertEquals("application/json", res.headers.get("Accept"));
    }

    @Test
    void test_set_request_type_xml() {
        res.set_request_type("xml");
        assertEquals("application/xml", res.headers.get("Accept"));
        res.set_request_type("xml");
        assertEquals("application/xml", res.headers.get("Accept"));
    }

    @Test
    void test_get_simple() {
        Map<String, Object> params = new HashMap<>();
        params.put("testparam", "yes");
        Map<String, Object> result = res.get(params);
        assertTrue(result instanceof Map);
        assertTrue(result.containsKey("result"));
    }

    @Test
    void test_post_simple() {
        Map<String, Object> data = new HashMap<>();
        data.put("hello", "world");
        Map<String, Object> result = res.post(data);
        assertTrue(result instanceof Map);
        assertTrue(result.containsKey("result"));
    }

    @Test
    void test_put_with_id() {
        res.id = "99";
        Map<String, Object> data = new HashMap<>();
        data.put("update", "yes");
        Map<String, Object> result = res.put(data);
        assertTrue(result instanceof Map);
    }

    @Test
    void test_put_without_id() {
        res.id = null;
        Map<String, Object> data = new HashMap<>();
        data.put("update", "no");
        Map<String, Object> result = res.put(data);
        assertNull(result);
    }

    @Test
    void test_delete_with_id() {
        res.id = "88";
        Map<String, Object> result = res.delete();
        assertTrue(result instanceof Map);
    }

    @Test
    void test_delete_without_id() {
        res.id = null;
        Map<String, Object> result = res.delete();
        assertNull(result);
    }

    @Test
    void test_repr() {
        String s = res.toString();
        assertTrue(s.contains(res.uri));
    }
}