package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;
import java.util.stream.Collectors;

class PublicCategorymembersTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testCategorymembersCount() {
        WikipediaApi.Page page = wiki.page("Category:C1");
        assertEquals(3, page.categorymembers.size());
    }

    @Test
    void testCategorymembersTitles() {
        WikipediaApi.Page page = wiki.page("Category:C1");
        List<String> titles = page.categorymembers.values().stream().map(p -> p.title).sorted().collect(Collectors.toList());
        List<String> expected = new ArrayList<>();
        for (int i = 1; i <= 3; i++) expected.add("Title - " + i);
        Collections.sort(expected);
        assertEquals(expected, titles);
    }
}