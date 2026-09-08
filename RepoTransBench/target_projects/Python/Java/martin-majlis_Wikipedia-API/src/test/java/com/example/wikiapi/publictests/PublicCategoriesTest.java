package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;
import java.util.stream.Collectors;

class PublicCategoriesTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testCategoriesCount() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals(3, page.categories.size());
    }

    @Test
    void testCategoriesTitles() {
        WikipediaApi.Page page = wiki.page("Test_1");
        List<String> titles = page.categories.values().stream().map(p -> p.title).sorted().collect(Collectors.toList());
        List<String> expected = new ArrayList<>();
        for (int i = 1; i <= 3; i++) expected.add("Category:C" + i);
        Collections.sort(expected);
        assertEquals(expected, titles);
    }
}