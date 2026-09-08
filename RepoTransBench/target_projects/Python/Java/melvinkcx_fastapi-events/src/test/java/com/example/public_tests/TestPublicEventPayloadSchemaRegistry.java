package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicEventPayloadSchemaRegistry {

    @Test
    void testRegisterSchema() {
        Registry reg = new Registry();
        assertTrue(reg.register("test-event", "SchemaA"));
        assertEquals("SchemaA", reg.get("test-event"));
    }

    @Test
    void testNoOverwrite() {
        Registry reg = new Registry();
        reg.register("event", "A");
        Exception ex = assertThrows(IllegalStateException.class, () -> reg.register("event", "B"));
        assertTrue(ex.getMessage().contains("already registered"));
    }

    @Test
    void testGetUnknownReturnsNull() {
        Registry reg = new Registry();
        assertNull(reg.get("not found"));
    }

    // Simulated schema registry for test
    private static class Registry {
        private final java.util.Map<String, String> store = new java.util.HashMap<>();
        boolean register(String evt, String sch) {
            if (store.containsKey(evt)) throw new IllegalStateException("already registered");
            store.put(evt, sch);
            return true;
        }
        String get(String evt) { return store.get(evt); }
    }
}