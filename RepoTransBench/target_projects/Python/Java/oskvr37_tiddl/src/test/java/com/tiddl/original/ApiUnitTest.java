package com.tiddl.original;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class ApiUnitTest {
    static class DummyApi {
        boolean error = false;
        int val = 123;
        int fetch(String endpoint) {
            if (error) throw new RuntimeException("unitfail");
            return val;
        }
        String fetchString(String endpoint) {
            return "response";
        }
    }
    @Test
    void test_fetch_ok() {
        DummyApi api = new DummyApi();
        assertEquals(123, api.fetch("endpoint"));
    }
    @Test
    void test_fetch_fail() {
        DummyApi api = new DummyApi();
        api.error = true;
        Exception ex = assertThrows(RuntimeException.class, () -> api.fetch("endpoint"));
        assertTrue(ex.getMessage().contains("unitfail"));
    }
    @Test
    void test_fetch_string() {
        DummyApi api = new DummyApi();
        assertEquals("response", api.fetchString("any"));
    }
}