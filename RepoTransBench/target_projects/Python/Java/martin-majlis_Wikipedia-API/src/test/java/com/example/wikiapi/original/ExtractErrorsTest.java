package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class ExtractErrorsTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testTitleBeforeFetching() {
        WikipediaApi.Page page = wiki.page("NonExisting");
        assertEquals("NonExisting", page.title);
    }

    @Test
    void testPageId() {
        WikipediaApi.Page page = wiki.page("NonExisting");
        assertEquals(-1, page.pageid);
    }
}