package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class PublicExtractErrorsTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testPageId() {
        WikipediaApi.Page page = wiki.page("NonExisting");
        assertEquals(-1, page.pageid);
    }
}