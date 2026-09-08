package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;
import java.util.stream.Collectors;

class LinksTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipedia();
    }

    @Test
    void testLinksSinglePageCount() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals(3, page.links.size());
    }

    @Test
    void testLinksSinglePageTitles() {
        WikipediaApi.Page page = wiki.page("Test_1");
        List<String> titles = page.links.values().stream().map(p -> p.title).sorted().collect(Collectors.toList());
        List<String> expected = new ArrayList<>();
        for (int i = 1; i <= 3; i++) {
            expected.add("Title - " + i);
        }
        Collections.sort(expected);
        assertEquals(expected, titles);
    }

    @Test
    void testLinksMultiPageCount() {
        WikipediaApi.Page page = wiki.page("Test_2");
        assertEquals(5, page.links.size());
    }

    @Test
    void testLinksMultiPageTitles() {
        WikipediaApi.Page page = wiki.page("Test_2");
        List<String> titles = page.links.values().stream().map(p -> p.title).sorted().collect(Collectors.toList());
        List<String> expected = new ArrayList<>();
        for (int i = 1; i <= 5; i++) {
            expected.add("Title - " + i);
        }
        Collections.sort(expected);
        assertEquals(expected, titles);
    }

    @Test
    void testLinksNoLinksCount() {
        WikipediaApi.Page page = wiki.page("No_Links");
        assertEquals(0, page.links.size());
    }

    @Test
    void testLinksFromVariant() {
        WikipediaApi.Wikipedia wikiVariant = WikipediaApi.MockFactory.makeWikipediaWithVariant("zh", "zh-tw");
        WikipediaApi.Page page = wikiVariant.page("Test_Zh-Tw");
        List<Map.Entry<String,String>> titlesVariants = page.links.values().stream()
            .map(p -> new AbstractMap.SimpleEntry<>(p.title, p.variant))
            .sorted(Comparator.comparing(Map.Entry::getKey))
            .collect(Collectors.toList());
        List<Map.Entry<String,String>> expected = new ArrayList<>();
        for (int i = 1; i <= 3; i++) {
            expected.add(new AbstractMap.SimpleEntry<>("Title - Zh-Tw - " + i, "zh-tw"));
        }
        expected.sort(Comparator.comparing(Map.Entry::getKey));
        assertEquals(expected, titlesVariants);
    }
}