package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;
import java.util.*;

class WikipediaPageTest {
    WikipediaApi.Wikipedia wiki = WikipediaApi.MockFactory.makeWikipedia();

    @Test
    void testComparisons() {
        WikipediaApi.Page page1a = wiki.page("Test_1");
        WikipediaApi.Page page1b = wiki.page("Test_1");
        WikipediaApi.Page page2 = wiki.page("Test_2");
        assertEquals(page1a, page1b);
        assertNotEquals(page1a, page2);
    }

    @Test
    void testReprContainsTitle() {
        WikipediaApi.Page page = wiki.page("Test_Title");
        String rep = page.toString();
        assertTrue(rep.contains("Test_Title"));
    }

    @Test
    void testHashEqual() {
        WikipediaApi.Page page1a = wiki.page("Test_1");
        WikipediaApi.Page page1b = wiki.page("Test_1");
        assertEquals(page1a.hashCode(), page1b.hashCode());
    }
}