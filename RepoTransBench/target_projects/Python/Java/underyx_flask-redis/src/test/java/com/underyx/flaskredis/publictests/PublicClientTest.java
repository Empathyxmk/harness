package com.underyx.flaskredis.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicClientTest {
    static class DummyRedis {
        static String url = null;
        static Map<String, Object> kwargs = null;
        public static Object from_url(String urlStr, Map<String, Object> kwargs_) {
            url = urlStr;
            kwargs = kwargs_;
            return new Object();
        }
    }

    @Test
    void testFlaskRedisInitAppDifferentUrl() {
        // Simulate a config map & monkeypatch
        class FlaskRedis {
            public String config_prefix = "APP2";
            public DummyRedis provider_class;
            public FlaskRedis(String prefix) { this.config_prefix = prefix; }
            public void initApp(Map<String,Object> app, String foo) {
                DummyRedis.from_url((String)app.get(this.config_prefix + "_URL"),
                        Map.of("foo", foo));
                app.put(this.config_prefix.toLowerCase(), this);
            }
        }
        Map<String, Object> app = new HashMap<>();
        app.put("APP2_URL", "redis://127.0.0.1:6382/5");
        new FlaskRedis("APP2").initApp(app, "barbazquux");
        assertEquals("redis://127.0.0.1:6382/5", DummyRedis.url);
        assertEquals("barbazquux", DummyRedis.kwargs.get("foo"));
        assertTrue(app.containsKey("app2"));
    }

    @Test
    void testFromCustomProviderDiffUrl() {
        class OtherProvider {
            static String called_url;
            static Map<String,Object> called_kwargs;
            public static Object from_url(String url, Map<String,Object> kwargs) {
                called_url = url;
                called_kwargs = kwargs;
                return "hello-ext";
            }
        }
        class FlaskRedis {
            public OtherProvider provider_class;
            public static FlaskRedis fromCustomProvider(Object provider, Map<String,Object> app, String baropt) {
                OtherProvider.from_url((String)app.get("REDIS_URL"), Map.of("baropt", baropt));
                app.put("redis", "self");
                return new FlaskRedis();
            }
        }
        Map<String,Object> app = new HashMap<>();
        app.put("REDIS_URL", "redis://192.168.1.2:6399/6");
        FlaskRedis.fromCustomProvider(new OtherProvider(), app, "bartest99");
        assertEquals("redis://192.168.1.2:6399/6", OtherProvider.called_url);
        assertEquals("bartest99", OtherProvider.called_kwargs.get("baropt"));
        assertTrue(app.containsKey("redis"));
    }

    @Test
    void testFlaskRedisBasicInstance() {
        class FlaskRedis {
            public String config_prefix;
            public FlaskRedis(String prefix) { config_prefix = prefix; }
        }
        FlaskRedis r = new FlaskRedis("BAR");
        assertEquals("BAR", r.config_prefix);
    }
}