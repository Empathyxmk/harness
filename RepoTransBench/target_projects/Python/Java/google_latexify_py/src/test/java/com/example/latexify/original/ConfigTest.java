package com.example.latexify.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class ConfigTest {

    // Simulates the Python latexify.config.Config object
    static class Config {
        Map<String, Object> values = new HashMap<>();
        boolean frozen = false;

        public void set(String key, Object value) {
            if (frozen) throw new IllegalStateException("Config is frozen");
            values.put(key, value);
        }

        public Object get(String key) {
            return values.get(key);
        }

        public void update(Map<String, Object> updates) {
            if (frozen) throw new IllegalStateException("Config is frozen");
            values.putAll(updates);
        }

        public void freeze() {
            frozen = true;
        }

        public boolean isFrozen() {
            return frozen;
        }
    }

    private Config config;

    @BeforeEach
    void setUp() {
        config = new Config();
        config.set("math_notation", true);
        config.set("inline", false);
    }

    @Test
    void testInitialConfigValues() {
        assertEquals(true, config.get("math_notation"));
        assertEquals(false, config.get("inline"));
    }

    @Test
    void testConfigSetAndGet() {
        config.set("math_notation", "yes");
        assertEquals("yes", config.get("math_notation"));
    }

    @Test
    void testUpdate() {
        Map<String, Object> updates = new HashMap<>();
        updates.put("inline", true);
        updates.put("display_mode", "block");
        config.update(updates);
        assertEquals(true, config.get("inline"));
        assertEquals("block", config.get("display_mode"));
    }

    @Test
    void testFreezePreventsModification() {
        config.freeze();
        assertTrue(config.isFrozen());
        Exception ex = assertThrows(IllegalStateException.class, () ->
            config.set("inline", true)
        );
        assertTrue(ex.getMessage().contains("frozen"));
    }

    @Test
    void testUpdateAfterFreezeThrows() {
        config.freeze();
        Map<String, Object> updates = new HashMap<>();
        updates.put("inline", true);
        Exception ex = assertThrows(IllegalStateException.class, () ->
            config.update(updates)
        );
        assertTrue(ex.getMessage().contains("frozen"));
    }
}