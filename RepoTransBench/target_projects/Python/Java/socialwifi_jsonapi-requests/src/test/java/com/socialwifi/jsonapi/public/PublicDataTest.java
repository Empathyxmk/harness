package com.socialwifi.jsonapi.public;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

public class PublicDataTest {

    static class Data {
        String id;
        String type;
        Map<String, Object> attributes;

        public Data(String id, String type, Map<String, Object> attributes) {
            this.id = id;
            this.type = type;
            this.attributes = attributes;
        }

        public Map<String, Object> asDict() {
            Map<String, Object> map = new HashMap<>();
            map.put("id", id);
            map.put("type", type);
            map.put("attributes", attributes);
            return map;
        }

        public static Data fromDict(Map<String, Object> map) {
            return new Data(
                    (String) map.get("id"),
                    (String) map.get("type"),
                    (Map<String, Object>) map.get("attributes")
            );
        }
    }

    @Test
    public void testAsDictRoundTrip() {
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("foo", 5);
        Data d = new Data("12", "thing", attrs);
        Map<String, Object> dict = d.asDict();
        assertEquals("12", dict.get("id"));
        assertEquals("thing", dict.get("type"));
        assertTrue(dict.containsKey("attributes"));
        assertEquals(5, ((Map<String, Object>)dict.get("attributes")).get("foo"));

        // Now, test round-trip
        Data from = Data.fromDict(dict);
        assertEquals("12", from.id);
        assertEquals("thing", from.type);
        assertEquals(5, from.attributes.get("foo"));
    }
}