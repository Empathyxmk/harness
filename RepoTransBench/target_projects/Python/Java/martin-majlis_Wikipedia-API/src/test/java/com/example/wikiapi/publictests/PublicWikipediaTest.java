package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

class PublicWikipediaTest {

    @Test
    void testSwappedParametersInConstructor() {
        AssertionError e = assertThrows(AssertionError.class, () -> {
            new WikipediaApi.Wikipedia("en", "my-user-agent");
        });
        assertTrue(e.getMessage().contains("Please, be nice to Wikipedia and specify user agent"));
    }
}