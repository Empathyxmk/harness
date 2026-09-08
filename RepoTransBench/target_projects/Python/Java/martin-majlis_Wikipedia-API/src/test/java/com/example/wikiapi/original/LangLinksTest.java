package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;
import java.util.stream.Collectors;

class LangLinksTest {
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

    @Test
    void testLanglinksKeys() {
        WikipediaApi.Page page = wiki.page("Test_LangLinks");
        List<String> keys = new ArrayList<>(page.langlinks.keySet());
        Collections.sort(keys);
        assertEquals(Arrays.asList("de", "es", "fr"), keys);
    }

    @Test
    void testLanglinksTitles() {
        WikipediaApi.Page page = wiki.page("Test_LangLinks");
        List<String> titles = page.langlinks.values().stream().map(p -> p.title).sorted().collect(Collectors.toList());
        List<String> expected = Arrays.asList("Page_de", "Page_es", "Page_fr");
        Collections.sort(expected);
        assertEquals(expected, titles);
    }
}