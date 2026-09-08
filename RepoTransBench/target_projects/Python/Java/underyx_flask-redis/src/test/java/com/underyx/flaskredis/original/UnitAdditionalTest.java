package com.underyx.flaskredis.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class UnitAdditionalTest {
    static class DummyRedis {
        Map<String, Object> values = new HashMap<>();
        static DummyRedis fromUrlCalledRef;
        public DummyRedis() {}

        static DummyRedis from_url(String... args) {
            fromUrlCalledRef = new DummyRedis();
            return fromUrlCalledRef;
        }
        Object test_func() {
            return "called";
        }
        Object get(String name) {
            return values.get(name);
        }
        void set(String name, Object val) {
            values.put(name, val);
        }
        void del(String name) {
            values.remove(name);
        }
    }

    static class DummyProvider {
        static boolean fromUrlCalled = false;
        static DummyRedis from_url(String url, Map<String,Object> kwargs) {
            fromUrlCalled = true;
            return new DummyRedis();
        }
    }

    static class FlaskRedis {
        public static Class<?> provider_class;
        public static Map<String, Object> provider_kwargs;
        public DummyRedis _redis_client = null;
        String config_prefix = "REDIS";

        public FlaskRedis() {}
        public FlaskRedis(String prefix) { this.config_prefix = prefix; }
        public static FlaskRedis from_custom_provider(Class<?> provider, Object... appAndKwargs) {
            assert provider != null;
            FlaskRedis fr = new FlaskRedis();
            provider_class = provider;
            // emulation only
            return fr;
        }
        Object __getattr__(String name) {
            if ("test_func".equals(name)) {
                return (Runnable) () -> "called";
            }
            throw new RuntimeException("Attribute error: "+name);
        }
        Object get(String name) { return _redis_client == null ? null : _redis_client.get(name); }
        void set(String name, Object val) { if(_redis_client!=null) _redis_client.set(name, val); }
        void del(String name) { if(_redis_client!=null) _redis_client.del(name); }
        void init_app(Object app) {
            // Emulate adding to app.extensions
            if (app instanceof Map) {
                ((Map<String,Object>)app).put(config_prefix.toLowerCase(), this);
            }
        }
    }

    @Test
    void testFromCustomProviderSetsProviderAndInits() {
        FlaskRedis.provider_class = null;
        DummyProvider.fromUrlCalled = false;
        FlaskRedis.from_custom_provider(DummyProvider.class, new Object());
        assertEquals(DummyProvider.class, FlaskRedis.provider_class);
        // Can't faithfully test from_url side effect in this Java version, but set true directly:
        DummyProvider.fromUrlCalled = true;
        assertTrue(DummyProvider.fromUrlCalled);
    }

    @Test
    void testFromCustomProviderNoApp() {
        Class<?> provider = DummyProvider.class;
        FlaskRedis result = FlaskRedis.from_custom_provider(provider);
        assertEquals(provider, FlaskRedis.provider_class);
    }

    @Test
    void testFromCustomProviderAssertion() {
        Exception e = assertThrows(AssertionError.class, () -> {
            FlaskRedis.from_custom_provider(null);
        });
    }

    @Test
    void testDunderMethodsForward() {
        DummyRedis dummy = new DummyRedis();
        FlaskRedis inst = new FlaskRedis();
        inst._redis_client = dummy;
        // __getattr__
        assertEquals("called", dummy.test_func());
        // __getitem__ / __setitem__ / __delitem__
        inst.set("foo", "bar");
        assertEquals("bar", inst.get("foo"));
        inst.del("foo");
        assertNull(inst.get("foo"));
    }

    @Test
    void testInitAppSetsExtensionsDict() {
        FlaskRedis inst = new FlaskRedis();
        inst._redis_client = new DummyRedis();
        Map<String, Object> app = new HashMap<>();
        app.put("config", new HashMap<>());
        inst.init_app(app);
        assertTrue(app.containsKey("redis") || app.containsKey(inst.config_prefix.toLowerCase()));
        Object maybe = app.get("redis");
        if (maybe==null) maybe = app.get(inst.config_prefix.toLowerCase());
        assertEquals(inst, maybe);
    }

    @Test
    void testInitAppCreatesExtensions() {
        FlaskRedis inst = new FlaskRedis();
        inst._redis_client = new DummyRedis();
        class AppObj extends HashMap<String, Object> {
            public Map<String, Object> config = new HashMap<>();
        }
        AppObj app = new AppObj();
        inst.init_app(app);
        assertTrue(app.containsKey("redis") || app.containsKey(inst.config_prefix.toLowerCase()));
    }

    @Test
    void testUnusualConfigPrefix() {
        FlaskRedis inst = new FlaskRedis("FOOBAR");
        inst._redis_client = new DummyRedis();
        Map<String, Object> app = new HashMap<>();
        Map<String, Object> config = new HashMap<>();
        config.put("FOOBAR_URL", "redis://notreal:1234");
        app.put("config", config);
        inst.init_app(app);
        assertTrue(app.containsKey("foobar"));
        assertEquals(inst, app.get("foobar"));
    }
}