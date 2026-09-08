package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.Map;
import java.util.HashMap;

public class HttpClientTest {

    @ParameterizedTest
    @ValueSource(ints = {
        100, 101, 102, 103,
        201, 202, 203, 204, 205, 206, 207, 208, 226,
        300, 301, 302, 303, 304, 305, 306, 307, 308,
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422,
        423, 424, 426, 428, 429, 431, 440, 444, 449, 450, 451, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598
    })
    void testHttpGetHandlerThrowsExceptionOnStatusDifferentOf200(int httpStatus) {
        HttpClient cli = spy(new HttpClient());
        DummyResponse resp = new DummyResponse(httpStatus, "http://some-url");
        doReturn(resp).when(cli).rawGet(anyString());

        NuRequestException ex = assertThrows(NuRequestException.class, () -> cli.get("http://some-url"));
        assertEquals(httpStatus, ex.getStatusCode());
        assertEquals("http://some-url", ex.getUrl());
        assertNotNull(ex.getResponse());
    }

    @ParameterizedTest
    @ValueSource(ints = {
        100, 101, 102, 103,
        201, 202, 203, 204, 205, 206, 207, 208, 226,
        300, 301, 302, 303, 304, 305, 306, 307, 308,
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422,
        423, 424, 426, 428, 429, 431, 440, 444, 449, 450, 451, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 520, 521, 522, 523, 524, 525, 526, 527, 530, 598
    })
    void testHttpPostHandlerThrowsExceptionOnStatusDifferentOf200(int httpStatus) {
        HttpClient cli = spy(new HttpClient());
        DummyResponse resp = new DummyResponse(httpStatus, "http://some-url");
        doReturn(resp).when(cli).rawPost(anyString(), any());
        NuRequestException ex = assertThrows(NuRequestException.class,
            () -> cli.post("http://some-url", new HashMap<>()));
        assertEquals(httpStatus, ex.getStatusCode());
        assertEquals("http://some-url", ex.getUrl());
        assertNotNull(ex.getResponse());
    }

    @Test
    void testGet() {
        HttpClient cli = spy(new HttpClient());
        Map<String, Object> json = new HashMap<>();
        json.put("key", 123);
        DummyResponse resp = new DummyResponse(200, "some-url", json, null);
        doReturn(resp).when(cli).rawGet(anyString());
        Map<String, Object> result = cli.get("some-url");
        assertEquals(123, result.get("key"));
    }

    @Test
    void testPost() {
        HttpClient cli = spy(new HttpClient());
        Map<String, Object> json = new HashMap<>();
        json.put("key", 555);
        DummyResponse resp = new DummyResponse(200, "some-url", json, null);
        doReturn(resp).when(cli).rawPost(anyString(), any());
        Map<String, Object> result = cli.post("some-url", new HashMap<>());
        assertEquals(555, result.get("key"));
    }

    @Test
    void testClientShouldClearHeadersOnNewInstance() {
        HttpClient cli1 = new HttpClient();
        cli1.setHeader("SomeHeader", "SomeValue");
        HttpClient cli2 = new HttpClient();
        cli2.setHeader("OtherHeader", "SomeValue");
        assertNull(cli2.getHeader("SomeHeader"));
        assertEquals("SomeValue", cli2.getHeader("OtherHeader"));
    }
}