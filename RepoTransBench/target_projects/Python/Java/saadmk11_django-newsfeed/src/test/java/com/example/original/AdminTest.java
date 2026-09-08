package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class AdminTest {

    // Simulate Django admin registration
    static class AdminRegistry {
        private Map<String, Object> registry = new HashMap<>();
        void register(String modelName, Object adminClass) {
            registry.put(modelName, adminClass);
        }
        boolean isRegistered(String modelName) {
            return registry.containsKey(modelName);
        }
        Object getAdmin(String modelName) {
            return registry.get(modelName);
        }
    }

    static class Post {}
    static class PostAdmin {}
    static class Issue {}
    static class IssueAdmin {}

    @Test
    void testModelsRegisteredWithAdmin() {
        AdminRegistry admin = new AdminRegistry();
        admin.register("Post", new PostAdmin());
        admin.register("Issue", new IssueAdmin());
        assertTrue(admin.isRegistered("Post"));
        assertTrue(admin.isRegistered("Issue"));
        assertTrue(admin.getAdmin("Post") instanceof PostAdmin);
        assertTrue(admin.getAdmin("Issue") instanceof IssueAdmin);
        assertFalse(admin.isRegistered("Subscriber")); // Not registered
    }
}