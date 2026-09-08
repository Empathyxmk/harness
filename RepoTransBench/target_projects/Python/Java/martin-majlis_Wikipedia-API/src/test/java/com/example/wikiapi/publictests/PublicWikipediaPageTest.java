package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class PublicWikipediaPageTest {

    WikipediaApi.Wikipedia wiki = WikipediaApi.MockFactory.makeWikipedia();

    @Test
    void testHashcodeForEquality() {
        WikipediaApi.Page page1 = wiki.page("Test_1");
        WikipediaApi.Page page2 = wiki.page("Test_1");
        assertEquals(page1.hashCode(), page2.hashCode());
    }
}