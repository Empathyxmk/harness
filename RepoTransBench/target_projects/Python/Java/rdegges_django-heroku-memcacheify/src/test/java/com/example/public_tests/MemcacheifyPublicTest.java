package com.example.public_tests;

import com.example.Memcacheify;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@TestInstance(TestInstance.Lifecycle.PER_METHOD)
public class MemcacheifyPublicTest {

    private Map<String, String> savedEnvVars;
    private static final List<String> ENV_VARS = Arrays.asList(
        "MEMCACHE_SERVERS",
        "MEMCACHE_USERNAME",
        "MEMCACHE_PASSWORD",
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
    public void testLocalMemcacheIsDefault() {
        Map<String, Object> result = Memcacheify.memcacheify();
        Object conf = result.get("default");
        assertTrue(conf instanceof Map);
        assertEquals("django.core.cache.backends.locmem.LocMemCache", ((Map<String, Object>) conf).get("BACKEND"));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testLocationFromMemcacheServers() {
        setEnv("MEMCACHE_SERVERS", "hostX:12345,hostY:54321");
        Map<String, Object> result = Memcacheify.memcacheify();
        Map<String, Object> conf = (Map<String, Object>) result.get("default");
        assertEquals(Arrays.asList("hostX:12345", "hostY:54321"), conf.get("LOCATION"));
        unsetEnv("MEMCACHE_SERVERS");
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
            // expected in some JVMs, harmless for CI
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
            // expected in some JVMs, harmless for CI
        }
    }
}