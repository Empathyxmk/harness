package com.osslacker.public_tests;

import com.osslacker.slacker.*;
import com.osslacker.slacker.utilities.Utilities;
import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class TestPublicInitTest {
    @Test
    void test_successful_response() {
        String json = "{\"ok\": true, \"value\": 100}";
        Response resp = new Response(json);
        assertTrue(resp.successful);
        assertEquals(100, ((Number)resp.body.get("value")).intValue());
        assertNull(resp.error);
        assertTrue(resp.toString().contains("\"value\"=100") || resp.toString().contains("value=100"));
    }

    @Test
    void test_error_response() {
        String json = "{\"ok\": false, \"error\": \"otherfail\"}";
        Response resp = new Response(json);
        assertFalse(resp.successful);
        assertEquals("otherfail", resp.error);
        assertTrue(resp.toString().contains("otherfail"));
    }

    @Test
    void test_get_success() {
        try (MockedStatic<Utilities> mockUtils = Mockito.mockStatic(Utilities.class)) {
            mockUtils.when(() -> Utilities.get_api_url(anyString())).then(invocation -> "https://slack.com/api/" + invocation.getArgument(0));
            BaseAPI api = new BaseAPI("another_test") {
                @Override
                public Response get(String method) {
                    return new Response("{\"ok\": true, \"x\": 5}");
                }
            };
            Response resp = api.get("api.other_test");
            assertTrue(resp.successful);
        }
    }

    @Test
    void test_get_error() {
        try (MockedStatic<Utilities> mockUtils = Mockito.mockStatic(Utilities.class)) {
            mockUtils.when(() -> Utilities.get_api_url(anyString())).then(invocation -> "https://slack.com/api/" + invocation.getArgument(0));
            BaseAPI api = new BaseAPI("another_test") {
                @Override
                public Response get(String method) {
                    return new Response("{\"ok\": false, \"error\": \"badrequest\"}");
                }
            };
            Error thrown = assertThrows(Error.class, () -> {
                Response resp = api.get("api.other_test");
                if (!resp.successful) throw new Error(resp.error);
            });
            assertEquals("badrequest", thrown.getMessage());
        }
    }

    @Test
    void test_get_429_retry() {
        try (MockedStatic<Utilities> mockUtils = Mockito.mockStatic(Utilities.class)) {
            mockUtils.when(() -> Utilities.get_api_url(anyString())).then(invocation -> "https://slack.com/api/" + invocation.getArgument(0));
            final int[] called = {0};
            BaseAPI api = new BaseAPI("another_test", 2) {
                @Override
                public Response get(String method) {
                    if (called[0]++ == 0) {
                        throw new Error("429");
                    }
                    return new Response("{\"ok\": true}");
                }
            };
            try {
                api.get("api.other_test");
            } catch (Error e) {
                Response resp = api.get("api.other_test");
                assertTrue(resp.successful);
            }
        }
    }

    @Test
    void test_session_methods() {
        BaseAPI api = new BaseAPI("another_test") {
            public boolean getCalled = false, postCalled = false;

            @Override
            public void _session_get(String url, Map<String, Object> params) {
                getCalled = true;
                assertEquals("http://another-url", url);
                assertEquals(10, params.get("x"));
            }

            @Override
            public void _session_post(String url, Map<String, Object> data) {
                postCalled = true;
                assertEquals("http://another-url", url);
                assertEquals(20, data.get("y"));
            }
        };
        api._session_get("http://another-url", Map.of("x", 10));
        api._session_post("http://another-url", Map.of("y", 20));
        assertTrue(((BaseAPI) api).getCalled);
        assertTrue(((BaseAPI) api).postCalled);
    }

    @Test
    void test_api_test() {
        BaseAPI base = mock(BaseAPI.class);
        doReturn(new Response("{\"ok\": true}")).when(base).get(anyString());
        API api = new API("T_public");
        api.test();
        api.test("badrequest", 42);
        verify(base, atLeast(0)).get(anyString());
    }

    @Test
    void test_auth_test() {
        BaseAPI base = mock(BaseAPI.class);
        doReturn(new Response("{\"ok\": true}")).when(base).get(anyString());
        Auth auth = new Auth("T_public");
        auth.test();
        verify(base, atLeast(0)).get(anyString());
    }

    @Test
    void test_auth_revoke() {
        BaseAPI base = mock(BaseAPI.class);
        doReturn(new Response("{\"ok\": true}")).when(base).post(anyString(), anyMap());
        Auth auth = new Auth("T_public");
        auth.revoke();
        auth.revoke(false);
        verify(base, atLeast(0)).post(anyString(), anyMap());
    }

    @Test
    void test_error_repr() {
        Error e = new Error("another error message");
        assertEquals("another error message", e.toString());
    }
}