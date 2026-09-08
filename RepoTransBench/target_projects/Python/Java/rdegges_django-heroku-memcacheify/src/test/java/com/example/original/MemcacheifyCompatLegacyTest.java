package com.example.original;

import com.example.Memcacheify;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@TestInstance(TestInstance.Lifecycle.PER_METHOD)
public class MemcacheifyCompatLegacyTest {

    private Map<String, String> savedEnvVars;
    private static final List<String> ENV_VARS = Arrays.asList(
        "MEMCACHE_SERVERS",
        "MEMCACHE_USERNAME",
        "MEMCACHE_PASSWORD",
        "MEMCACHIER_SERVERS",
        "MEMCACHIER_USERNAME",
        "MEMCACHIER_PASSWORD",
        "MEMCACHEDCLOUD_SERVERS",
        "MEMCACHEDCLOUD_USERNAME",
        "MEMCACHEDCLOUD_PASSWORD",
        "MEMCACHEIFY_USE_LOCAL"
    );

    @BeforeEach
    void setUp() {
        savedEnvVars = new HashMap<>();
        for (String key : ENV_VARS) {
            String val = System.getenv(key);
            if (val != null) savedEnvVars.put(key, val);
            unsetEnv(key);
        }
    }

    @AfterEach
    void tearDown() {
        for (String key : ENV_VARS) {
            unsetEnv(key);
        }
        for (Map.Entry<String, String> e : savedEnvVars.entrySet()) {
            setEnv(e.getKey(), e.getValue());
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testMemcachierEnvForwardsToMemcacheVars() {
        setEnv("MEMCACHIER_SERVERS", "mc.serv1,mc.serv2");
        setEnv("MEMCACHIER_USERNAME", "user57");
        setEnv("MEMCACHIER_PASSWORD", "pw58");
        Map<String, Object> result = Memcacheify.memcacheify();
        Map<String, Object> conf = (Map<String, Object>) result.get("default");
        assertEquals("django_pylibmc.memcached.PyLibMCCache", conf.get("BACKEND"));
        assertEquals("mc.serv1,mc.serv2", System.getenv("MEMCACHE_SERVERS"));
        assertEquals("user57", System.getenv("MEMCACHE_USERNAME"));
        assertEquals("pw58", System.getenv("MEMCACHE_PASSWORD"));
        unsetEnv("MEMCACHIER_SERVERS");
        unsetEnv("MEMCACHIER_USERNAME");
        unsetEnv("MEMCACHIER_PASSWORD");
        unsetEnv("MEMCACHE_SERVERS");
        unsetEnv("MEMCACHE_USERNAME");
        unsetEnv("MEMCACHE_PASSWORD");
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testMemcachedCloudEnvForwardsToMemcacheVars() {
        setEnv("MEMCACHEDCLOUD_SERVERS", "clserv1,clserv2");
        setEnv("MEMCACHEDCLOUD_USERNAME", "cloudU");
        setEnv("MEMCACHEDCLOUD_PASSWORD", "cloudP");
        Map<String, Object> result = Memcacheify.memcacheify();
        Map<String, Object> conf = (Map<String, Object>) result.get("default");
        assertEquals("django_pylibmc.memcached.PyLibMCCache", conf.get("BACKEND"));
        assertEquals("clserv1,clserv2", System.getenv("MEMCACHE_SERVERS"));
        assertEquals("cloudU", System.getenv("MEMCACHE_USERNAME"));
        assertEquals("cloudP", System.getenv("MEMCACHE_PASSWORD"));
        unsetEnv("MEMCACHEDCLOUD_SERVERS");
        unsetEnv("MEMCACHEDCLOUD_USERNAME");
        unsetEnv("MEMCACHEDCLOUD_PASSWORD");
        unsetEnv("MEMCACHE_SERVERS");
        unsetEnv("MEMCACHE_USERNAME");
        unsetEnv("MEMCACHE_PASSWORD");
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testDefaultsToLocal() {
        Map<String, Object> result = Memcacheify.memcacheify();
        Object conf = result.get("default");
        assertTrue(conf instanceof Map);
        assertEquals("django.core.cache.backends.locmem.LocMemCache", ((Map<String, Object>) conf).get("BACKEND"));
    }

    private void setEnv(String key, String value) {
        try {
            Map<String, String> env = System.getenv();
            java.lang.reflect.Field field = env.getClass().getDeclaredField("m");
            field.setAccessible(true);
            @SuppressWarnings("unchecked")
            Map<String, String> writable = (Map<String, String>) field.get(env);
            writable.put(key, value);
        } catch (Exception e) {
            // Ignore expected failures on modern JVMs.
        }
    }

    private void unsetEnv(String key) {
        try {
            Map<String, String> env = System.getenv();
            java.lang.reflect.Field field = env.getClass().getDeclaredField("m");
            field.setAccessible(true);
            @SuppressWarnings("unchecked")
            Map<String, String> writable = (Map<String, String>) field.get(env);
            writable.remove(key);
        } catch (Exception e) {
            // Ignore expected failures on modern JVMs.
        }
    }
}