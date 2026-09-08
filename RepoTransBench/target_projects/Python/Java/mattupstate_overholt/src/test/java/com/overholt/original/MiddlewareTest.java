package com.overholt.original;

import com.overholt.middleware.HTTPMethodOverrideMiddleware;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class DummyAppImpl implements HTTPMethodOverrideMiddleware.DummyApp {
    private Map<String, Object> lastEnviron;
    private List<Map.Entry<String, String>> lastHeaders;

    @Override
    public List<byte[]> call(Map<String, Object> environ, HTTPMethodOverrideMiddleware.StartResponse startResponse) {
        this.lastEnviron = environ;
        this.lastHeaders = new ArrayList<>();
        startResponse.call("200 OK", List.of(Map.entry("Content-Type", "text/plain")));
        return List.of("response".getBytes());
    }

    @Override
    public Map<String, Object> getLastEnviron() {
        return lastEnviron;
    }

    @Override
    public List<Map.Entry<String, String>> getLastHeaders() {
        return lastHeaders;
    }
}

public class MiddlewareTest {

    private Map<String, Object> makeEnviron(String method, String queryString, Map<String, String> headers) {
        Map<String, Object> environ = new HashMap<>();
        environ.put("REQUEST_METHOD", method);
        environ.put("QUERY_STRING", queryString == null ? "" : queryString);
        if (headers != null)
            environ.putAll(headers);
        return environ;
    }

    @Test
    void testMethodOverrideHeader() {
        DummyAppImpl app = new DummyAppImpl();
        HTTPMethodOverrideMiddleware middleware = new HTTPMethodOverrideMiddleware(app);
        Map<String, Object> environ = makeEnviron("POST", "", Map.of("HTTP_X_HTTP_METHOD_OVERRIDE", "DELETE"));
        final List<String> called = new ArrayList<>();
        HTTPMethodOverrideMiddleware.StartResponse startResp = (status, headers) -> called.add(status);
        List<byte[]> result = middleware.call(environ, startResp);

        Object reqMethod = app.getLastEnviron().get("REQUEST_METHOD");
        assertTrue(reqMethod instanceof byte[] && Arrays.equals((byte[])reqMethod, "DELETE".getBytes()));
        assertTrue(app.getLastEnviron().containsKey("CONTENT_LENGTH"));
        assertEquals(1, result.size());
        assertEquals("response", new String(result.get(0)));
        assertEquals("200 OK", called.get(0));
    }

    @Test
    void testMethodOverrideQuerystring() {
        DummyAppImpl app = new DummyAppImpl();
        HTTPMethodOverrideMiddleware middleware = new HTTPMethodOverrideMiddleware(app);
        Map<String, Object> environ = makeEnviron("POST", "foo=bar&__METHOD__=PUT", null);
        final List<String> called = new ArrayList<>();
        HTTPMethodOverrideMiddleware.StartResponse startResp = (status, headers) -> called.add(status);
        List<byte[]> result = middleware.call(environ, startResp);

        Object reqMethod = app.getLastEnviron().get("REQUEST_METHOD");
        assertTrue(reqMethod instanceof byte[] && Arrays.equals((byte[])reqMethod, "PUT".getBytes()));
        assertTrue(app.getLastEnviron().containsKey("CONTENT_LENGTH"));
        assertEquals(1, result.size());
        assertEquals("response", new String(result.get(0)));
    }

    @Test
    void testNoOverride() {
        DummyAppImpl app = new DummyAppImpl();
        HTTPMethodOverrideMiddleware middleware = new HTTPMethodOverrideMiddleware(app);
        Map<String, Object> environ = makeEnviron("GET", "", null);
        final List<String> called = new ArrayList<>();
        HTTPMethodOverrideMiddleware.StartResponse startResp = (status, headers) -> called.add(status);
        List<byte[]> result = middleware.call(environ, startResp);

        Object reqMethod = app.getLastEnviron().get("REQUEST_METHOD");
        assertTrue(reqMethod instanceof String && reqMethod.equals("GET"));
        assertEquals(1, result.size());
        assertEquals("response", new String(result.get(0)));
    }

    @Test
    void testOverrideWithCustom() {
        DummyAppImpl app = new DummyAppImpl();
        HTTPMethodOverrideMiddleware middleware = new HTTPMethodOverrideMiddleware(
            app, "X-MY-HEADER", "__MY_METHOD__", List.of("PUT")
        );
        Map<String, Object> environ = makeEnviron("POST", "", Map.of("HTTP_X_MY_HEADER", "PUT"));
        final List<String> called = new ArrayList<>();
        HTTPMethodOverrideMiddleware.StartResponse startResp = (status, headers) -> called.add(status);
        List<byte[]> result = middleware.call(environ, startResp);

        Object reqMethod = app.getLastEnviron().get("REQUEST_METHOD");
        assertTrue(reqMethod instanceof byte[] && Arrays.equals((byte[])reqMethod, "PUT".getBytes()));
    }

    @Test
    void testOverrideNotAllowed() {
        DummyAppImpl app = new DummyAppImpl();
        HTTPMethodOverrideMiddleware middleware = new HTTPMethodOverrideMiddleware(app, "X-HTTP-METHOD-OVERRIDE", "__METHOD__", Set.of("POST"));
        Map<String, Object> environ = makeEnviron("POST", "", Map.of("HTTP_X_HTTP_METHOD_OVERRIDE", "PATCH"));
        final List<String> called = new ArrayList<>();
        HTTPMethodOverrideMiddleware.StartResponse startResp = (status, headers) -> called.add(status);
        List<byte[]> result = middleware.call(environ, startResp);

        Object reqMethod = app.getLastEnviron().get("REQUEST_METHOD");
        assertTrue(reqMethod instanceof String && reqMethod.equals("POST"));
    }

    @Test
    void testGetFromQuerystringReturnsNone() {
        DummyAppImpl app = new DummyAppImpl();
        HTTPMethodOverrideMiddleware middleware = new HTTPMethodOverrideMiddleware(app);
        Map<String, Object> environ = makeEnviron("POST", "foo=bar", null);
        assertNull(middleware._getFromQuerystring(environ));
    }
}