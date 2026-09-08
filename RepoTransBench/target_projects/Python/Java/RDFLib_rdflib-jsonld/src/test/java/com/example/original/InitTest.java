package com.example.original;

import com.example.rdflibjsonld.RdflibJsonld;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from Python tests/test_init.py
 */
public class InitTest {

    @Test
    public void testImportRdflibJsonld() {
        // Essentially, check all public fields exist
        assertNotNull(RdflibJsonld.__doc__);
        assertNotNull(RdflibJsonld.__version__);
        assertNotNull(RdflibJsonld.__author__);
        assertNotNull(RdflibJsonld.__contact__);
        assertNotNull(RdflibJsonld.__docformat__);
    }
}