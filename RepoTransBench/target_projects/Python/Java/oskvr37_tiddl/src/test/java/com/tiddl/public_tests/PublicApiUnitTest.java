package com.tiddl.public_tests;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicApiUnitTest {

    static class DummyApi {
        boolean error = false;
        int val = 999;
        int fetch(String endpoint) {
            if (error) throw new RuntimeException("fail");
            return val;
        }
    }

    @Test
    void test_fetch_success() {
        DummyApi api = new DummyApi();
        assertEquals(999, api.fetch("endpoint"));
    }

    @Test
    void test_fetch_failure() {
        DummyApi api = new DummyApi();
        api.error = true;
        Exception ex = assertThrows(RuntimeException.class, () -> api.fetch("endpoint"));
        assertTrue(ex.getMessage().contains("fail"));
    }
}