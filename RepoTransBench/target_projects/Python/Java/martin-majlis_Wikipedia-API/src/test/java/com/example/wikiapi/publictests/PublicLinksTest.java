package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class PublicLinksTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testLinksCount() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals(3, page.links.size());
    }
}