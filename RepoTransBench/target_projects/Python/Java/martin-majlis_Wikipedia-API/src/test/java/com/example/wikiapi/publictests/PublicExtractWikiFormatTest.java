package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class PublicExtractWikiFormatTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipediaWithFormat(WikipediaApi.ExtractFormat.WIKI);
    }

    @Test
    void testSummary() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals("'''Summary''' text\n\n", page.summary);
    }

    @Test
    void testSectionCount() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals(5, page.sections.size());
    }
}