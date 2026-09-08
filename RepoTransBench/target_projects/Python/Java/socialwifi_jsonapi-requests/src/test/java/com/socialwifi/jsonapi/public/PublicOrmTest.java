package com.socialwifi.jsonapi.public;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

public class PublicOrmTest {

    static class SimpleModel {
        private String id;
        private String type;
        private Map<String, Object> attributes;

        public SimpleModel(String id, String type, Map<String, Object> attributes) {
            this.id = id;
            this.type = type;
            this.attributes = attributes;
        }

        public Map<String, Object> asData() {
            Map<String, Object> data = new HashMap<>();
            data.put("id", id);
            data.put("type", type);
            data.put("attributes", attributes);
            return data;
        }

        public static SimpleModel fromData(Map<String, Object> data) {
            String id = (String) data.get("id");
            String type = (String) data.get("type");
            Map<String, Object> attrs = (Map<String, Object>) data.get("attributes");
            return new SimpleModel(id, type, attrs);
        }
    }

    @Test
    public void testModelDataConversion() {
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("foo", "bar");
        SimpleModel model = new SimpleModel("5", "test", attrs);

        Map<String, Object> data = model.asData();
        assertEquals("5", data.get("id"));
        assertEquals("test", data.get("type"));
        assertTrue(((Map<?, ?>)data.get("attributes")).containsKey("foo"));

        // Now round-trip
        SimpleModel recovered = SimpleModel.fromData(data);
        assertEquals("5", recovered.id);
        assertEquals("test", recovered.type);
        assertEquals("bar", recovered.attributes.get("foo"));
    }

    @Test
    public void testBasicRelationships() {
        Map<String, Object> relationship = Map.of("data", Map.of("type", "other", "id", "44"));
        Map<String, Object> data = new HashMap<>();
        data.put("id", "55");
        data.put("type", "demo-model");
        data.put("relationships", Map.of("relname", relationship));

        SimpleModel m = SimpleModel.fromData(data);
        assertEquals("55", m.id);
        assertEquals("demo-model", m.type);
        // No explicit relationship mapping in dummy, just confirming object instantiates and id present
        assertEquals("55", m.id);
    }
}