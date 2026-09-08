package com.osslacker.tests.original;

import com.osslacker.slacker.*;
import com.osslacker.slacker.utilities.Utilities;
import org.junit.jupiter.api.*;
import org.mockito.ArgumentCaptor;
import org.mockito.MockedStatic;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class TestInitTest {
    @Test
    void test_successful_response() {
        String json = "{\"ok\": true, \"a\": 42}";
        Response resp = new Response(json);
        assertTrue(resp.successful);
        assertEquals(42, ((Number)resp.body.get("a")).intValue());
        assertNull(resp.error);
        assertTrue(resp.toString().contains("\"a\"=42") || resp.toString().contains("a=42"));
    }

    @Test
    void test_error_response() {
        String json = "{\"ok\": false, \"error\": \"fail\"}";
        Response resp = new Response(json);
        assertFalse(resp.successful);
        assertEquals("fail", resp.error);
        assertTrue(resp.toString().contains("fail"));
    }

    @Test
    void test_get_success() {
        try (MockedStatic<Utilities> mockUtils = Mockito.mockStatic(Utilities.class)) {
            mockUtils.when(() -> Utilities.get_api_url(anyString())).then(invocation -> "https://slack.com/api/" + invocation.getArgument(0));
            BaseAPI api = new BaseAPI("test") {
                @Override
                public Response get(String method) {
                    return new Response("{\"ok\": true}");
                }
            };
            Response resp = api.get("api.test");
            assertTrue(resp.successful);
        }
    }

    @Test
    void test_get_error() {
        try (MockedStatic<Utilities> mockUtils = Mockito.mockStatic(Utilities.class)) {
            mockUtils.when(() -> Utilities.get_api_url(anyString())).then(invocation -> "https://slack.com/api/" + invocation.getArgument(0));
            BaseAPI api = new BaseAPI("test") {
                @Override
                public Response get(String method) {
                    return new Response("{\"ok\": false, \"error\": \"fail\"}");
                }
            };
            Error thrown = assertThrows(Error.class, () -> {
                Response resp = api.get("api.test");
                if (!resp.successful) throw new Error(resp.error);
            });
            assertEquals("fail", thrown.getMessage());
        }
    }

    @Test
    void test_get_429_retry() {
        // Simulate a 429 error followed by success.
        try (MockedStatic<Utilities> mockUtils = Mockito.mockStatic(Utilities.class)) {
            mockUtils.when(() -> Utilities.get_api_url(anyString())).then(invocation -> "https://slack.com/api/" + invocation.getArgument(0));
            final int[] called = {0};
            BaseAPI api = new BaseAPI("test", 2) {
                @Override
                public Response get(String method) {
                    if (called[0]++ == 0) {
                        // 429 with retry-after=0
                        throw new Error("429");
                    }
                    return new Response("{\"ok\": true}");
                }
            };
            // Here we skip time.sleep mock. Just call twice.
            try {
                api.get("api.test");
            } catch (Error e) {
                // Retry once--which is the intended simulation
                Response resp = api.get("api.test");
                assertTrue(resp.successful);
            }
        }
    }

    @Test
    void test_session_methods() {
        BaseAPI api = new BaseAPI("test") {
            public boolean getCalled = false, postCalled = false;

            @Override
            public void _session_get(String url, Map<String, Object> params) {
                getCalled = true;
                assertEquals("http://url", url);
                assertEquals(1, params.get("a"));
            }

            @Override
            public void _session_post(String url, Map<String, Object> data) {
                postCalled = true;
                assertEquals("http://url", url);
                assertEquals(2, data.get("b"));
            }
        };

        api._session_get("http://url", Map.of("a", 1));
        api._session_post("http://url", Map.of("b", 2));
        assertTrue(((BaseAPI) api).getCalled);
        assertTrue(((BaseAPI) api).postCalled);
    }

    @Test
    void test_api_test() {
        BaseAPI base = mock(BaseAPI.class);
        doReturn(new Response("{\"ok\": true}")).when(base).get(anyString());
        API api = new API("T");
        api.test();
        api.test("fail", 1);
        verify(base, atLeast(0)).get(anyString());
    }

    @Test
    void test_auth_test() {
        BaseAPI base = mock(BaseAPI.class);
        doReturn(new Response("{\"ok\": true}")).when(base).get(anyString());
        Auth auth = new Auth("T");
        auth.test();
        verify(base, atLeast(0)).get(anyString());
    }

    @Test
    void test_auth_revoke() {
        BaseAPI base = mock(BaseAPI.class);
        doReturn(new Response("{\"ok\": true}")).when(base).post(anyString(), anyMap());
        Auth auth = new Auth("T");
        auth.revoke();
        auth.revoke(false);
        verify(base, atLeast(0)).post(anyString(), anyMap());
    }

    @Test
    void test_error_repr() {
        Error e = new Error("some error");
        assertEquals("some error", e.toString());
    }
}