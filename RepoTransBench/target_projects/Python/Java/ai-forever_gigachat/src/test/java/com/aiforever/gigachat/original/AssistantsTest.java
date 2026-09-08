package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class Assistant {
    String id;
    String name;
    String description;
    Map<String, Object> metadata;

    public Assistant(String id, String name, String description, Map<String, Object> metadata) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.metadata = metadata;
    }
}

public class AssistantsTest {
    @Test
    void testAssistantCreation() {
        Map<String, Object> meta = new HashMap<>();
        meta.put("lang", "en");
        Assistant a = new Assistant("asst_123", "Alice", "Math assistant", meta);
        assertEquals("Alice", a.name);
        assertEquals("Math assistant", a.description);
        assertEquals("en", a.metadata.get("lang"));
    }

    @Test
    void testAssistantFieldsNotNull() {
        Assistant a = new Assistant("id42", "Bob", "Helps", new HashMap<>());
        assertNotNull(a.id);
        assertNotNull(a.name);
        assertNotNull(a.description);
        assertNotNull(a.metadata);
    }

    @Test
    void testAssistantMetadata() {
        Map<String, Object> meta = Map.of("key", "value", "flag", true);
        Assistant a = new Assistant("id12", "Tom", "Desc", meta);
        assertTrue(a.metadata.containsKey("key"));
        assertTrue((Boolean) a.metadata.get("flag"));
    }
}