package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class PublicNamespaceAndExtractFormatTest {
    @Test
    void testNamespaceValue() {
        int nsValue = WikipediaApi.Namespace.FILE.id();
        assertNotEquals(0, nsValue);
    }
}