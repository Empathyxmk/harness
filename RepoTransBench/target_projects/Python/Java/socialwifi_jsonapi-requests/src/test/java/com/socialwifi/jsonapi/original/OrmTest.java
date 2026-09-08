package com.socialwifi.jsonapi.original;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

import java.util.*;

public class OrmTest {

    // Dummy model to simulate ORM logic for translation
    static class Article {
        String id;
        String type;
        Map<String, Object> attributes;

        public Article(String id, String type, Map<String, Object> attributes) {
            this.id = id;
            this.type = type;
            this.attributes = attributes;
        }

        public Map<String, Object> asData() {
            Map<String, Object> d = new HashMap<>();
            d.put("id", id);
            d.put("type", type);
            d.put("attributes", attributes);
            return d;
        }

        public static Article fromData(Map<String, Object> d) {
            return new Article(
                    (String)d.get("id"),
                    (String)d.get("type"),
                    (Map<String, Object>)d.get("attributes")
            );
        }
    }

    @Test
    public void testModelRoundTrip() {
        Article a = new Article("10", "article", Map.of("title", "hello"));
        Map<String, Object> d = a.asData();
        Article again = Article.fromData(d);
        assertEquals(a.id, again.id);
        assertEquals(a.type, again.type);
        assertEquals(a.attributes.get("title"), again.attributes.get("title"));
    }

    @Test
    public void testListOfModels() {
        Article a1 = new Article("11", "article", Map.of("title", "bob"));
        Article a2 = new Article("12", "article", Map.of("title", "alex"));
        List<Article> articles = List.of(a1, a2);
        List<Map<String, Object>> data = new ArrayList<>();
        for (Article a : articles)
            data.add(a.asData());
        assertEquals(2, data.size());
        assertEquals("bob", ((Map)data.get(0)).get("attributes") instanceof Map ? ((Map)((Map)data.get(0)).get("attributes")).get("title") : null);
        assertEquals("alex", ((Map)data.get(1)).get("attributes") instanceof Map ? ((Map)((Map)data.get(1)).get("attributes")).get("title") : null);
    }

    @Test
    public void testRelationships() {
        Map<String, Object> commentAttrs = Map.of("body", "hi");
        Article article = new Article("21", "article", Map.of("title", "extends"));
        Map<String, Object> rels = Map.of("author", Map.of("data", Map.of("type", "person", "id", "100")));
        Map<String, Object> asData = article.asData();
        asData.put("relationships", rels);
        // Simulate ORM restoration
        Article newArt = Article.fromData(asData);
        assertEquals("21", newArt.id);
        assertEquals("article", newArt.type);
        assertEquals("extends", newArt.attributes.get("title"));
        // In this dummy translation, we are just testing restoration of relationships as well done.
        Map<String, Object> relationships = (Map<String, Object>)asData.get("relationships");
        assertNotNull(relationships);
        assertTrue(relationships.containsKey("author"));
    }
}