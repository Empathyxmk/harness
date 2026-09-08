package com.socialwifi.jsonapi.public;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

public class PublicOrmExtraTest {

    static class ModelWithList {
        String id, type;
        List<String> tags;
        public ModelWithList(String id, String type, List<String> tags) {
            this.id = id;
            this.type = type;
            this.tags = tags;
        }

        public Map<String, Object> asData() {
            Map<String, Object> d = new HashMap<>();
            d.put("id", id);
            d.put("type", type);
            d.put("attributes", Map.of("tags", tags));
            return d;
        }

        public static ModelWithList fromData(Map<String, Object> d) {
            Map<String, Object> attrs = (Map)d.get("attributes");
            return new ModelWithList((String)d.get("id"), (String)d.get("type"),
                    (List<String>)attrs.get("tags"));
        }
    }

    @Test
    public void testListAttribute() {
        List<String> tags = Arrays.asList("a", "b", "c");
        ModelWithList mdl = new ModelWithList("90", "tagged", tags);
        Map<String, Object> data = mdl.asData();
        assertEquals(tags, ((Map)data.get("attributes")).get("tags"));
        ModelWithList mdl2 = ModelWithList.fromData(data);
        assertEquals(tags, mdl2.tags);
        assertEquals("90", mdl2.id);
    }
}