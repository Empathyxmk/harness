package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class PublicWikipediaObjectTest {

    WikipediaApi.Wikipedia wiki = WikipediaApi.MockFactory.makeWikipedia();

    @Test
    void testEqualsForSameTitlePages() {
        WikipediaApi.Page page1 = wiki.page("Test_1");
        WikipediaApi.Page page2 = wiki.page("Test_1");
        assertEquals(page1, page2);
    }

    @Test
    void testNotEqualsForDifferentPages() {
        WikipediaApi.Page page1 = wiki.page("Test_1");
        WikipediaApi.Page page2 = wiki.page("Test_2");
        assertNotEquals(page1, page2);
    }
}