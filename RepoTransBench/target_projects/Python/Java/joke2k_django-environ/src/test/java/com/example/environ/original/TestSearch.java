package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestSearch {

    @Test
    void testDefaultSearchConfig() {
        SearchConfig config = SearchConfig.defaultSearch();
        assertEquals("simple", config.getBackend());
    }

    @Test
    void testParseSearchUrl() {
        SearchConfig config = SearchConfig.fromUrl("elasticsearch://search.local:9200");
        assertEquals("elasticsearch", config.getBackend());
        assertEquals("search.local:9200", config.getLocation());
    }
}