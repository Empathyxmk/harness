package com.example.original;

import com.example.Memcacheify;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@TestInstance(TestInstance.Lifecycle.PER_METHOD)
public class MemcacheifyOriginalTest {

    private Map<String, String> savedEnvVars;
    private static final List<String> ENV_VARS = Arrays.asList(
        "MEMCACHE_SERVERS",
        "MEMCACHE_USERNAME",
        "MEMCACHE_PASSWORD",
        "MEMCACHEIFY_USE_LOCAL"
    );

    @BeforeEach
    void setUp() throws Exception {
        savedEnvVars = new HashMap<>();
        for (String key : ENV_VARS) {
            String val = System.getenv(key);
            if (val != null) savedEnvVars.put(key, val);
            unsetEnv(key);
        }
    }

    @AfterEach
    void tearDown() throws Exception {
        for (String key : ENV_VARS) {
            unsetEnv(key);
        }
        for (Map.Entry<String, String> e : savedEnvVars.entrySet()) {
            setEnv(e.getKey(), e.getValue());
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testDefaultIsLocMemCache() {
        Map<String, Object> result = Memcacheify.memcacheify();
        Object conf = result.get("default");
        assertTrue(conf instanceof Map);
        assertEquals("django.core.cache.backends.locmem.LocMemCache", ((Map<String, Object>) conf).get("BACKEND"));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testMemcacheServersTakesPrecedence() {
        setEnv("MEMCACHE_SERVERS", "server1:11211,server2:11211");
        setEnv("MEMCACHE_USERNAME", "myuser");
        setEnv("MEMCACHE_PASSWORD", "mypass");
        Map<String, Object> result = Memcacheify.memcacheify();
        Map<String, Object> conf = (Map<String, Object>) result.get("default");
        assertEquals("django_pylibmc.memcached.PyLibMCCache", conf.get("BACKEND"));
        assertEquals(Arrays.asList("server1:11211", "server2:11211"), conf.get("LOCATION"));
        Map<String, Object> options = (Map<String, Object>) conf.get("OPTIONS");
        assertEquals("myuser", options.get("username"));
        assertEquals("mypass", options.get("password"));
        unsetEnv("MEMCACHE_SERVERS");
        unsetEnv("MEMCACHE_USERNAME");
        unsetEnv("MEMCACHE_PASSWORD");
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testUseLocalForcesLocMemCache() {
        setEnv("MEMCACHEIFY_USE_LOCAL", "true");
        setEnv("MEMCACHE_SERVERS", "server:11");
        setEnv("MEMCACHE_USERNAME", "a");
        setEnv("MEMCACHE_PASSWORD", "pw");
        Map<String, Object> result = Memcacheify.memcacheify();
        Map<String, Object> conf = (Map<String, Object>) result.get("default");
        assertEquals("django.core.cache.backends.locmem.LocMemCache", conf.get("BACKEND"));
        assertFalse(conf.containsKey("LOCATION"));
        unsetEnv("MEMCACHEIFY_USE_LOCAL");
        unsetEnv("MEMCACHE_SERVERS");
        unsetEnv("MEMCACHE_USERNAME");
        unsetEnv("MEMCACHE_PASSWORD");
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
            // Can be ignored for most JVMs used in CI
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
            // Can be ignored for most JVMs used in CI
        }
    }
}