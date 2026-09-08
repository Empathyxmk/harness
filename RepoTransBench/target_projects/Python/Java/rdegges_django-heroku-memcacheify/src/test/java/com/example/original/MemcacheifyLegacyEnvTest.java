package com.example.original;

import com.example.Memcacheify;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@TestInstance(TestInstance.Lifecycle.PER_METHOD)
public class MemcacheifyLegacyEnvTest {

    private final List<String> relevantEnvs = Arrays.asList(
        "MEMCACHE_SERVERS", "MEMCACHE_USERNAME", "MEMCACHE_PASSWORD",
        "MEMCACHIER_SERVERS", "MEMCACHIER_USERNAME", "MEMCACHIER_PASSWORD",
        "MEMCACHEDCLOUD_SERVERS", "MEMCACHEDCLOUD_USERNAME", "MEMCACHEDCLOUD_PASSWORD",
        "MEMCACHEIFY_USE_LOCAL"
    );

    private Map<String, String> saved;

    @BeforeEach
    public void setUp() {
        saved = new HashMap<>();
        for (String k : relevantEnvs) {
            String v = System.getenv(k);
            if (v != null) saved.put(k, v);
            unsetEnv(k);
        }
    }

    @AfterEach
    public void tearDown() {
        for (String k : relevantEnvs) {
            unsetEnv(k);
        }
        for (Map.Entry<String, String> e : saved.entrySet()) {
            setEnv(e.getKey(), e.getValue());
        }
    }

    @SuppressWarnings("unchecked")
    @Test
    public void testUsesLocalCacheIfEnvEmpty() {
        Map<String, Object> result = Memcacheify.memcacheify();
        Object conf = result.get("default");
        assertTrue(conf instanceof Map);
        assertEquals("django.core.cache.backends.locmem.LocMemCache", ((Map<String, Object>) conf).get("BACKEND"));
    }

    @SuppressWarnings("unchecked")
    @Test
    public void testMemcachierSetsMemcacheVars() {
        setEnv("MEMCACHIER_SERVERS", "a,b,c");
        setEnv("MEMCACHIER_USERNAME", "u");
        setEnv("MEMCACHIER_PASSWORD", "pw");
        Map<String, Object> result = Memcacheify.memcacheify();
        Map<String, Object> conf = (Map<String, Object>) result.get("default");
        assertEquals("django_pylibmc.memcached.PyLibMCCache", conf.get("BACKEND"));
        assertEquals("a,b,c", System.getenv("MEMCACHE_SERVERS"));
        assertEquals("u", System.getenv("MEMCACHE_USERNAME"));
        assertEquals("pw", System.getenv("MEMCACHE_PASSWORD"));
        unsetEnv("MEMCACHIER_SERVERS");
        unsetEnv("MEMCACHIER_USERNAME");
        unsetEnv("MEMCACHIER_PASSWORD");
        unsetEnv("MEMCACHE_SERVERS");
        unsetEnv("MEMCACHE_USERNAME");
        unsetEnv("MEMCACHE_PASSWORD");
    }

    @SuppressWarnings("unchecked")
    @Test
    public void testMemcachedCloudSetsMemcacheVars() {
        setEnv("MEMCACHEDCLOUD_SERVERS", "cloud1,cloud2");
        setEnv("MEMCACHEDCLOUD_USERNAME", "clouduser");
        setEnv("MEMCACHEDCLOUD_PASSWORD", "cloudpass");
        Map<String, Object> result = Memcacheify.memcacheify();
        Map<String, Object> conf = (Map<String, Object>) result.get("default");
        assertEquals("django_pylibmc.memcached.PyLibMCCache", conf.get("BACKEND"));
        assertEquals("cloud1,cloud2", System.getenv("MEMCACHE_SERVERS"));
        assertEquals("clouduser", System.getenv("MEMCACHE_USERNAME"));
        assertEquals("cloudpass", System.getenv("MEMCACHE_PASSWORD"));
        unsetEnv("MEMCACHEDCLOUD_SERVERS");
        unsetEnv("MEMCACHEDCLOUD_USERNAME");
        unsetEnv("MEMCACHEDCLOUD_PASSWORD");
        unsetEnv("MEMCACHE_SERVERS");
        unsetEnv("MEMCACHE_USERNAME");
        unsetEnv("MEMCACHE_PASSWORD");
    }

    private void setEnv(String key, String value) {
        try {
            Map<String, String> env = System.getenv();
            java.lang.reflect.Field field = env.getClass().getDeclaredField("m");
            field.setAccessible(true);
            Map<String, String> writable = (Map<String, String>) field.get(env);
            writable.put(key, value);
        } catch (Exception e) {
            // Java 9+ fallback is tricky; tests will work in common CI environment
        }
    }

    private void unsetEnv(String key) {
        try {
            Map<String, String> env = System.getenv();
            java.lang.reflect.Field field = env.getClass().getDeclaredField("m");
            field.setAccessible(true);
            Map<String, String> writable = (Map<String, String>) field.get(env);
            writable.remove(key);
        } catch (Exception e) {
            // Java 9+ fallback is tricky; tests will work in common CI environment
        }
    }
}