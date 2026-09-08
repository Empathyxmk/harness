package com.underyx.flaskredis.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;

class IntegrationClientTest {

    static class FakeRedisClient {
        public Map<String, Object> connection_pool = Map.of("connection_kwargs", new HashMap<String, Object>());
        FakeRedisClient() {}
    }

    static class FlaskRedis {
        public FakeRedisClient _redis_client = null;
        public String config_prefix = "REDIS";
        public FlaskRedis() {}
        public FlaskRedis(Object app) {
            initApp(app);
        }
        public FlaskRedis(Object app, String config_prefix) {
            this.config_prefix = config_prefix;
            initApp(app);
        }
        public void initApp(Object app) {
            this._redis_client = new FakeRedisClient();
            if (app instanceof Map) {
                ((Map<String,Object>)app).put(this.config_prefix.toLowerCase(), this);
            }
        }
        public Map<String,Object> connection_pool() {
            return _redis_client.connection_pool;
        }

        static class StrictFakeRedisClient extends FakeRedisClient {}
        static FlaskRedis from_custom_provider(Class<?> provider, Object... appAndKwargs) {
            return new FlaskRedis();
        }
    }

    @Test
    void testConstructor() {
        Map<String, Object> app = new HashMap<>();
        FlaskRedis redis = new FlaskRedis(app);
        assertNotNull(redis._redis_client);
        assertNotNull(redis._redis_client.connection_pool);
    }

    @Test
    void testInitApp() {
        Map<String, Object> app = new HashMap<>();
        FlaskRedis redis = new FlaskRedis();
        assertNull(redis._redis_client);
        redis.initApp(app);
        assertNotNull(redis._redis_client);
        assertNotNull(redis._redis_client.connection_pool);
        assertTrue(app.containsKey(redis.config_prefix.toLowerCase()));
        assertEquals(redis, app.get(redis.config_prefix.toLowerCase()));
    }

    @Test
    void testCustomPrefix() {
        Map<String, Object> app = new HashMap<>();
        Map<String,Object> config = new HashMap<>();
        config.put("DBA_URL", "redis://localhost:6379/1");
        config.put("DBB_URL", "redis://localhost:6379/2");
        app.put("config", config);

        FlaskRedis redisA = new FlaskRedis(app, "DBA");
        ((HashMap)((FakeRedisClient)redisA._redis_client).connection_pool.get("connection_kwargs")).put("db", 1);
        FlaskRedis redisB = new FlaskRedis(app, "DBB");
        ((HashMap)((FakeRedisClient)redisB._redis_client).connection_pool.get("connection_kwargs")).put("db", 2);

        assertEquals(1, ((HashMap)((FakeRedisClient)redisA._redis_client).connection_pool.get("connection_kwargs")).get("db"));
        assertEquals(2, ((HashMap)((FakeRedisClient)redisB._redis_client).connection_pool.get("connection_kwargs")).get("db"));
    }

    @Test
    void testStrictParameter() {
        // strict_flag == true
        class StrictFakeRedisClient extends FakeRedisClient {}
        // Only "StrictRedis" and "Redis"
        for (boolean strict_flag : new boolean[]{true, false}) {
            FlaskRedis redis = new FlaskRedis();
            redis._redis_client = strict_flag ? new StrictFakeRedisClient() : new FakeRedisClient();
            String name = redis._redis_client.getClass().getSimpleName();
            if (strict_flag) {
                assertTrue(name.equals("StrictFakeRedisClient") || name.equals("StrictRedis") || name.equals("Redis"));
            } else {
                assertTrue(name.equals("FakeRedisClient") || name.equals("Redis"));
            }
        }
    }

    @Test
    void testCustomProvider() {
        class FakeProvider {
            static boolean fromUrlCalled = false;
            static FakeProvider from_url(String url, Map<String,Object> kwargs) {
                fromUrlCalled = true;
                return new FakeProvider();
            }
        }
        Map<String, Object> app = new HashMap<>();
        FlaskRedis redis = FlaskRedis.from_custom_provider(FakeProvider.class);
        assertNull(redis._redis_client);
        redis.initApp(app);
        redis._redis_client = new FakeRedisClient();
        assertNotNull(redis._redis_client);
        assertTrue(redis._redis_client instanceof FakeRedisClient);
    }
}