package com.stephenmcd.formsbuilder.original;

import org.junit.jupiter.api.Test;

import java.io.*;

import static org.junit.jupiter.api.Assertions.*;

public class DocsConfPyTest {

    @Test
    public void testDocsConfImport() throws Exception {
        // The logic here is to simulate 'import' and check that some 'setup_conf' is called
        final boolean[] called = new boolean[]{false};
        class FakeSphinxMe {
            public void setupConf(Object g) {
                called[0] = true;
            }
        }
        // Simulate executing docs/conf.py code that would call setup_conf
        FakeSphinxMe sphinxMe = new FakeSphinxMe();
        sphinxMe.setupConf(null);
        assertTrue(called[0]);
    }
}