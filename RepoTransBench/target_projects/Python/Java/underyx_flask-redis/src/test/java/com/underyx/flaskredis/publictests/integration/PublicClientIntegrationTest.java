package com.underyx.flaskredis.publictests.integration;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicClientIntegrationTest {
    static class DummyRedis {
        static String calledWithUrl;
        static Map<String, Object> calledWithKwargs;
        public static Object from_url(String url, Map<String, Object> kwargs) {
            calledWithUrl = url;
            calledWithKwargs = kwargs;
            return new Object();
        }
    }

    @Test
    void testInitAppCustomUrlPublic() {
        class FlaskRedis {
            public String config_prefix = "FOO";
            public DummyRedis provider_class;
            public void initApp(Map<String, Object> app, String password) {
                DummyRedis.from_url((String)app.get(this.config_prefix + "_URL"),
                        Map.of("password", password));
                app.put(this.config_prefix.toLowerCase(), this);
            }
        }
        Map<String, Object> app = new HashMap<>();
        app.put("FOO_URL", "redis://localhost:6380/2");
        new FlaskRedis().initApp(app, "letmein");
        assertEquals("redis://localhost:6380/2", DummyRedis.calledWithUrl);
        assertEquals("letmein", DummyRedis.calledWithKwargs.get("password"));
        assertTrue(app.containsKey("foo"));
    }

    @Test
    void testFromCustomProviderPublic() {
        class CustomProvider {
            static String last_url;
            static Map<String,Object> last_kwargs;
            public static Object from_url(String url, Map<String,Object> kwargs) {
                last_url = url;
                last_kwargs = kwargs;
                return "custom-conn";
            }
        }
        class FlaskRedis {
            public static FlaskRedis fromCustomProvider(Object provider, Map<String,Object> app, int fooopt) {
                CustomProvider.from_url((String)app.get("REDIS_URL"), Map.of("fooopt", fooopt));
                app.put("redis", "self");
                return new FlaskRedis();
            }
        }
        Map<String,Object> app = new HashMap<>();
        app.put("REDIS_URL", "redis://localhost:6381/4");
        FlaskRedis.fromCustomProvider(new CustomProvider(), app, 99);
        assertEquals("redis://localhost:6381/4", CustomProvider.last_url);
        assertEquals(99, CustomProvider.last_kwargs.get("fooopt"));
        assertTrue(app.containsKey("redis"));
    }
}