package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class WikipediaObjectTest {
    @Test
    void testWikipediaInitMinimal() {
        WikipediaApi.Wikipedia wiki = new WikipediaApi.Wikipedia("test/1.0", "en");
        assertNotNull(wiki);
        assertEquals("en", wiki.getLanguage());
        assertEquals(WikipediaApi.ExtractFormat.WIKI, wiki.getExtractFormat());
    }

    @Test
    void testWikipediaInitAllArgs() {
        WikipediaApi.Wikipedia wiki = new WikipediaApi.Wikipedia(
                "test/2.0",
                "de",
                "bar",
                WikipediaApi.ExtractFormat.HTML,
                Map.of("Foo", "Bar"),
                Map.of("baz", "qux"),
                1
        );
        assertEquals("de", wiki.getLanguage());
        assertEquals("bar", wiki.getVariant());
        assertEquals(WikipediaApi.ExtractFormat.HTML, wiki.getExtractFormat());
    }

    @Test
    void testWikipediaInitShortUserAgentRaises() {
        Exception exception = assertThrows(Exception.class, () ->
                new WikipediaApi.Wikipedia("bot", "en")
        );
    }
}