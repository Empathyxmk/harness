package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;

class PublicLanglinksTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testLanglinksCount() {
        WikipediaApi.Page page = wiki.page("Test_LangLinks");
        assertEquals(3, page.langlinks.size());
    }
}