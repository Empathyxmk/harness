package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class PublicConfigTest {

    // Public user accessible config imitation
    static class PublicConfig {
        private Map<String, Object> fields = new HashMap<>();

        public PublicConfig() {
            fields.put("inline", false);
        }
        public Object get(String k) {
            return fields.get(k);
        }
        public void set(String k, Object v) {
            fields.put(k, v);
        }
    }

    @Test
    void testDefaultInline() {
        PublicConfig cfg = new PublicConfig();
        assertEquals(false, cfg.get("inline"));
    }

    @Test
    void testSetInline() {
        PublicConfig cfg = new PublicConfig();
        cfg.set("inline", true);
        assertEquals(true, cfg.get("inline"));
    }
}