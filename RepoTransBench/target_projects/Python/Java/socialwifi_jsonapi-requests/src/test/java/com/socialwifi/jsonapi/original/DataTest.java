package com.socialwifi.jsonapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

public class DataTest {

    static class Data {
        String id;
        String type;
        Map<String, Object> attributes;

        public Data(String id, String type, Map<String, Object> attributes) {
            this.id = id;
            this.type = type;
            this.attributes = attributes;
        }

        public Map<String, Object> toMap() {
            Map<String, Object> map = new HashMap<>();
            map.put("id", id);
            map.put("type", type);
            map.put("attributes", attributes);
            return map;
        }

        public static Data fromMap(Map<String, Object> map) {
            return new Data(
                    (String) map.get("id"),
                    (String) map.get("type"),
                    (Map<String, Object>) map.get("attributes")
            );
        }
    }

    @Test
    public void testToMapAndFromMap() {
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("value", 42);
        Data d = new Data("100", "number", attrs);
        Map<String, Object> map = d.toMap();
        assertEquals("100", map.get("id"));
        assertEquals("number", map.get("type"));
        assertEquals(42, ((Map<String, Object>) map.get("attributes")).get("value"));

        Data again = Data.fromMap(map);
        assertEquals("100", again.id);
        assertEquals("number", again.type);
        assertEquals(42, again.attributes.get("value"));
    }

    @Test
    public void testEmptyAttributes() {
        Data d = new Data("101", "empty", Collections.emptyMap());
        Map<String, Object> map = d.toMap();
        assertTrue(((Map<String, Object>) map.get("attributes")).isEmpty());
    }
}