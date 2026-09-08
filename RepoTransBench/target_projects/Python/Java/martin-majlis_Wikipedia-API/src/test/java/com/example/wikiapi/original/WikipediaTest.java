package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class WikipediaTest {

    @Test
    void testMissingUserAgentShouldFail() {
        AssertionError e = assertThrows(AssertionError.class, () -> {
            new WikipediaApi.Wikipedia("en");
        });
        String msg = "Please, be nice to Wikipedia and specify user agent - " +
                "https://meta.wikimedia.org/wiki/User-Agent_policy. " +
                "Current user_agent: 'en' is not sufficient. " +
                "Use Wikipedia(user_agent='your-user-agent', language='en')";
        assertEquals(msg, e.getMessage());
    }

    @Test
    void testSwappedParametersInConstructor() {
        AssertionError e = assertThrows(AssertionError.class, () -> {
            new WikipediaApi.Wikipedia("en", "my-user-agent");
        });
        String msg = "Please, be nice to Wikipedia and specify user agent - " +
                "https://meta.wikimedia.org/wiki/User-Agent_policy. " +
                "Current user_agent: 'en' is not sufficient. " +
                "Use Wikipedia(user_agent='your-user-agent', language='en')";
        assertEquals(msg, e.getMessage());
    }

    @Test
    void testEmptyParametersInConstructor() {
        AssertionError e = assertThrows(AssertionError.class, () -> {
            new WikipediaApi.Wikipedia("", "");
        });
        String msg = "Please, be nice to Wikipedia and specify user agent - " +
                "https://meta.wikimedia.org/wiki/User-Agent_policy. " +
                "Current user_agent: '' is not sufficient. " +
                "Use Wikipedia(user_agent='your-user-agent', language='your-language')";
        assertEquals(msg, e.getMessage());
    }

    @Test
    void testEmptyLanguageInConstructor() {
        AssertionError e = assertThrows(AssertionError.class, () -> {
            new WikipediaApi.Wikipedia("test-user-agent", "");
        });
        String msg = "Specify language. Current language: '' is not sufficient. " +
                "Use Wikipedia(user_agent='test-user-agent', language='your-language')";
        assertEquals(msg, e.getMessage());
    }

    @Test
    void testLongLanguageAndUserAgent() {
        WikipediaApi.Wikipedia wiki = new WikipediaApi.Wikipedia("param-user-agent", "very-long-language");
        assertNotNull(wiki);
        assertEquals("very-long-language", wiki.getLanguage());
        assertNull(wiki.getVariant());
    }

    @Test
    void testUserAgentIsUsed() {
        WikipediaApi.Wikipedia wiki = new WikipediaApi.Wikipedia("param-user-agent");
        assertNotNull(wiki);
        String userAgent = wiki.getSessionHeader("User-Agent");
        assertEquals("param-user-agent (" + WikipediaApi.USER_AGENT + ")", userAgent);
        assertEquals("en", wiki.getLanguage());
    }

    @Test
    void testUserAgentInHeadersIsFine() {
        WikipediaApi.Wikipedia wiki = new WikipediaApi.Wikipedia("en",
                Map.of("User-Agent", "header-user-agent"));
        assertNotNull(wiki);
        String userAgent = wiki.getSessionHeader("User-Agent");
        assertEquals("header-user-agent (" + WikipediaApi.USER_AGENT + ")", userAgent);
    }

    @Test
    void testUserAgentInHeadersWin() {
        WikipediaApi.Wikipedia wiki = new WikipediaApi.Wikipedia("param-user-agent",
                Map.of("User-Agent", "header-user-agent"));
        assertNotNull(wiki);
        String userAgent = wiki.getSessionHeader("User-Agent");
        assertEquals("header-user-agent (" + WikipediaApi.USER_AGENT + ")", userAgent);
    }
}