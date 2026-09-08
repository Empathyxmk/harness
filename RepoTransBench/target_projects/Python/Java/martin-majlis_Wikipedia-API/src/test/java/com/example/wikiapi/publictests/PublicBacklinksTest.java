package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;
import java.util.*;
import java.util.stream.Collectors;

class PublicBacklinksTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testSinglePageBacklinksCount() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals(3, page.backlinks.size());
    }

    @Test
    void testSinglePageBacklinksTitles() {
        WikipediaApi.Page page = wiki.page("Test_1");
        List<String> titles = page.backlinks.values().stream()
            .map(p -> p.title).sorted().collect(Collectors.toList());
        List<String> expected = new ArrayList<>();
        for (int i = 1; i <= 3; i++) expected.add("Backlink - " + i);
        Collections.sort(expected);
        assertEquals(expected, titles);
    }
}