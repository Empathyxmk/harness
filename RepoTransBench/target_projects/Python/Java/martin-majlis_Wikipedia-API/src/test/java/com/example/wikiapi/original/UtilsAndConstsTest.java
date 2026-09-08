package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class UtilsAndConstsTest {

    @Test
    void testConstantsAreSet() {
        assertTrue(WikipediaApi.USER_AGENT instanceof String);
        assertTrue(WikipediaApi.USER_AGENT.length() > 10);
        assertTrue(Integer.class.isInstance(WikipediaApi.MIN_USER_AGENT_LEN));
        assertTrue(Integer.class.isInstance(WikipediaApi.MAX_LANG_LEN));
    }

    @Test
    void testReSectionPatterns() {
        assertTrue(WikipediaApi.RE_SECTION.get(WikipediaApi.ExtractFormat.WIKI).pattern().startsWith("\\n\\n"));
        assertTrue(WikipediaApi.RE_SECTION.get(WikipediaApi.ExtractFormat.HTML).pattern().startsWith("\\n? *<h([1-9])"));
    }
}