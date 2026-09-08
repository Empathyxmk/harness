package com.example.public_tests;

import com.example.rdflibjsonld.RdflibJsonld;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from public_tests/test_public_init.py
 */
public class PublicInitTest {

    @Test
    public void testImportRdflibJsonldPublic() {
        assertTrue(RdflibJsonld.__doc__ == null || RdflibJsonld.__doc__ instanceof String);
        assertTrue(RdflibJsonld.__version__ instanceof String);
        assertTrue(RdflibJsonld.__author__ instanceof String);
        assertTrue(RdflibJsonld.__contact__ instanceof String);
        assertTrue(RdflibJsonld.__docformat__ instanceof String);
    }
}