package com.example.wikiapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class NamespaceAndExtractFormatTest {
    @Test
    void testNamespaceEnumMembers() {
        assertEquals(0, WikipediaApi.Namespace.MAIN.getValue());
        assertEquals(2, WikipediaApi.Namespace.USER.getValue());
        assertEquals(14, WikipediaApi.Namespace.CATEGORY.getValue());
        assertEquals(108, WikipediaApi.Namespace.BOOK.getValue());
        assertEquals(2300, WikipediaApi.Namespace.GADGET.getValue());
    }

    @Test
    void testExtractFormatEnumMembers() {
        assertEquals(1, WikipediaApi.ExtractFormat.WIKI.getValue());
        assertEquals(2, WikipediaApi.ExtractFormat.HTML.getValue());
    }

    @Test
    void testNamespace2IntWithEnum() {
        assertEquals(0, WikipediaApi.namespace2int(WikipediaApi.Namespace.MAIN));
        assertEquals(14, WikipediaApi.namespace2int(WikipediaApi.Namespace.CATEGORY));
    }

    @Test
    void testNamespace2IntWithInt() {
        assertEquals(42, WikipediaApi.namespace2int(42));
        assertEquals(0, WikipediaApi.namespace2int(0));
    }

    @Test
    void testInvalidNamespace2Int() {
        // Should not throw
        assertEquals(WikipediaApi.Namespace.USER_TALK.getValue(),
                     WikipediaApi.namespace2int(WikipediaApi.Namespace.USER_TALK));
    }

    @Test
    void testExtractFormatRepr() {
        assertEquals("WIKI", WikipediaApi.ExtractFormat.WIKI.name());
        assertEquals("HTML", WikipediaApi.ExtractFormat.HTML.name());
    }
}