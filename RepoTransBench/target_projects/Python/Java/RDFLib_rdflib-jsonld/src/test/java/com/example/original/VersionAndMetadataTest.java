package com.example.original;

import com.example.rdflibjsonld.RdflibJsonld;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from Python tests/test_version_and_metadata.py
 */
public class VersionAndMetadataTest {

    @Test
    public void testVersionDefined() {
        assertNotNull(RdflibJsonld.__version__);
        assertTrue(RdflibJsonld.__version__ instanceof String);
        assertEquals("0.6.2", RdflibJsonld.__version__);
    }

    @Test
    public void testAuthorDefined() {
        assertNotNull(RdflibJsonld.__author__);
        assertTrue(RdflibJsonld.__author__ instanceof String);
        assertTrue(RdflibJsonld.__author__.contains("RDFLib"));
    }

    @Test
    public void testContactDefined() {
        assertNotNull(RdflibJsonld.__contact__);
        assertTrue(RdflibJsonld.__contact__ instanceof String);
        assertTrue(RdflibJsonld.__contact__.contains("@"));
    }

    @Test
    public void testDocformatDefined() {
        assertNotNull(RdflibJsonld.__docformat__);
        assertEquals("restructuredtext", RdflibJsonld.__docformat__);
    }

    @Test
    public void testModuleDocstringExists() {
        String doc = RdflibJsonld.__doc__;
        assertNotNull(doc);
        String lower = doc.trim().toLowerCase();
        assertTrue(
                lower.contains("plugin for rdflib") || lower.contains("a plugin for rdflib"),
                "Docstring should mention plugin for rdflib"
        );
    }
}