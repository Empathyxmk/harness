package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;
import java.util.stream.Collectors;

class CategoriesTest {
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

    @Test
    void testCategoriesNs() {
        WikipediaApi.Page page = wiki.page("Test_1");
        List<Integer> nss = page.categories.values().stream().map(p -> p.ns).sorted().collect(Collectors.toList());
        List<Integer> expected = Arrays.asList(14, 14, 14);
        assertEquals(expected, nss);
    }

    @Test
    void testNoCategoriesCount() {
        WikipediaApi.Page page = wiki.page("No_Categories");
        assertEquals(0, page.categories.size());
    }
}