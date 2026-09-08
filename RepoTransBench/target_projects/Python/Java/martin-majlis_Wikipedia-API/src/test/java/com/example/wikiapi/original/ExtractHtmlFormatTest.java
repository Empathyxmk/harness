package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;
import java.util.stream.Collectors;

class ExtractHtmlFormatTest {
    WikipediaApi.Wikipedia wiki;

    @BeforeEach
    void setUp() {
        wiki = WikipediaApi.MockFactory.makeWikipediaWithFormat(WikipediaApi.ExtractFormat.HTML);
    }

    @Test
    void testTitleBeforeFetching() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals("Test_1", page.title);
    }

    @Test
    void testPageId() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals(4, page.pageid);
    }

    @Test
    void testTitleAfterFetching() {
        WikipediaApi.Page page = wiki.page("Test_1");
        page._fetch("extracts");
        assertEquals("Test 1", page.title);
    }

    @Test
    void testSummary() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals("<p><b>Summary</b> text\n\n</p>", page.summary);
    }

    @Test
    void testSectionCount() {
        WikipediaApi.Page page = wiki.page("Test_1");
        assertEquals(5, page.sections.size());
    }

    @Test
    void testTopLevelSectionTitles() {
        WikipediaApi.Page page = wiki.page("Test_1");
        List<String> titles = page.sections.stream().map(s -> s.title).collect(Collectors.toList());
        List<String> expected = new ArrayList<>();
        for (int i = 1; i <= 5; i++) expected.add("Section " + i);
        assertEquals(expected, titles);
    }

    @Test
    void testSubsectionByTitle() {
        WikipediaApi.Page page = wiki.page("Test_1");
        WikipediaApi.Section section = page.sectionByTitle("Section 4");
        assertEquals("Section 4", section.title);
        assertEquals(1, section.level);
    }

    @Test
    void testSubsectionByTitleWithMultipleSpans() {
        WikipediaApi.Page page = wiki.page("Test_1");
        WikipediaApi.Section section = page.sectionByTitle("Section 5");
        assertEquals("Section 5", section.title);
    }

    @Test
    void testSubsection() {
        WikipediaApi.Page page = wiki.page("Test_1");
        WikipediaApi.Section section = page.sectionByTitle("Section 4");
        assertEquals("Section 4", section.title);
        assertEquals("", section.text);
        assertEquals(2, section.sections.size());
    }

    @Test
    void testSubsubsection() {
        WikipediaApi.Page page = wiki.page("Test_1");
        WikipediaApi.Section section = page.sectionByTitle("Section 4.2.2");
        assertEquals("Section 4.2.2", section.title);
        assertEquals("<p><b>Text for section 4.2.2</b>\n\n\n</p>", section.text);
        assertEquals("Section: Section 4.2.2 (3):\n" +
            "<p><b>Text for section 4.2.2</b>\n\n\n</p>\n" +
            "Subsections (0):\n"
            , section.toString());
        assertEquals(0, section.sections.size());
    }

    @Test
    void testSubsectionByTitleReturnLast() {
        WikipediaApi.Page page = wiki.page("Test_Nested");
        WikipediaApi.Section section = page.sectionByTitle("Subsection B");
        assertEquals("Subsection B", section.title);
        assertEquals("<p><b>Text for section 3.B</b>\n\n\n</p>", section.text);
        assertEquals(0, section.sections.size());
    }

    @Test
    void testSubsectionsByTitle() {
        WikipediaApi.Page page = wiki.page("Test_Nested");
        List<WikipediaApi.Section> sections = page.sectionsByTitle("Subsection B");
        assertEquals(3, sections.size());
        List<String> texts = new ArrayList<>();
        for (WikipediaApi.Section s : sections) texts.add(s.text);
        List<String> expected = Arrays.asList(
            "<p><b>Text for section 1.B</b>\n\n\n</p>",
            "<p><b>Text for section 2.B</b>\n\n\n</p>",
            "<p><b>Text for section 3.B</b>\n\n\n</p>"
        );
        assertEquals(expected, texts);
    }

    @Test
    void testText() {
        WikipediaApi.Page page = wiki.page("Test_1");
        String expected = "<p><b>Summary</b> text\n\n</p>\n\n" +
                "<h2>Section 1</h2>\n<p>Text for section 1</p>\n\n" +
                "<h3>Section 1.1</h3>\n<p><b>Text for section 1.1</b>\n\n\n</p>\n\n" +
                "<h3>Section 1.2</h3>\n<p><b>Text for section 1.2</b>\n\n\n</p>\n\n" +
                "<h2>Section 2</h2>\n<p><b>Text for section 2</b>\n\n\n</p>\n\n" +
                "<h2>Section 3</h2>\n<p><b>Text for section 3</b>\n\n\n</p>\n\n" +
                "<h2>Section 4</h2>\n<h3>Section 4.1</h3>\n<p><b>Text for section 4.1</b>\n\n\n</p>\n\n" +
                "<h3>Section 4.2</h3>\n<p><b>Text for section 4.2</b>\n\n\n</p>\n\n" +
                "<h4>Section 4.2.1</h4>\n<p><b>Text for section 4.2.1</b>\n\n\n</p>\n\n" +
                "<h4>Section 4.2.2</h4>\n<p><b>Text for section 4.2.2</b>\n\n\n</p>\n\n" +
                "<h2>Section 5</h2>\n<p><b>Text for section 5</b>\n\n\n</p>\n\n" +
                "<h3>Section 5.1</h3>\n<p>Text for section 5.1\n\n\n</p>";
        assertEquals(expected, page.text);
    }

    @Test
    void testWithErroneousEdit() {
        WikipediaApi.Page page = wiki.page("Test_Edit");
        WikipediaApi.Section section = page.sectionByTitle("Section with Edit");
        assertEquals("Section with Edit", section.title);
        String expected = "<p><b>Summary</b> text\n\n</p>\n\n" +
                "<h2>Section 1</h2>\n<p>Text for section 1</p>\n\n" +
                "<h3>Section with Edit</h3>\n<p>Text for section with edit\n\n\n</p>";
        assertEquals(expected, page.text);
    }
}