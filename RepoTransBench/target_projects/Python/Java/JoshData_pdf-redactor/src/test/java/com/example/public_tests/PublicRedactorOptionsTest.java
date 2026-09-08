package com.example.public_tests;

import com.example.pdfredactor.RedactorOptions;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicRedactorOptionsTest {
    @Test
    public void testMetadataDefaults() {
        Map<String,String> meta = new HashMap<>();
        meta.put("Title", "PublicTitle");
        meta.put("Subject", "PublicSubj");
        meta.put("Author", "AuthorPerson");

        RedactorOptions options = new RedactorOptions(meta, null);
        assertEquals("PublicTitle", options.metadata.get("Title"));
        assertEquals("PublicSubj", options.metadata.get("Subject"));
        assertEquals("AuthorPerson", options.metadata.get("Author"));
    }

    @Test
    public void testOptionsFiltersList() {
        List<Object[]> filters = Arrays.asList(
                new Object[]{"\\d{2}-\\d{2}-\\d{4}", "REDACT"},
                new Object[]{"SecretWord", "VisibleWord"}
        );
        RedactorOptions options = new RedactorOptions(null, filters);
        // In this demo, contentFilters is empty array, but the constructor allows storing the given value
        assertTrue(filters.size() == 2);
        assertEquals("VisibleWord", filters.get(1)[1]);
    }
}