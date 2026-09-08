package org.commoncrawl.stormcrawler;

import org.junit.Test;
import static org.junit.Assert.*;

public class FastURLFilterPublicTest {

    @Test
    public void testDifferentDomainURLAllowed() {
        FastURLFilter filter = new FastURLFilter();
        assertTrue(filter.isAllowed("https://anotherdomain.com/index.html"));
    }

    @Test
    public void testFilteredExtension() {
        FastURLFilter filter = new FastURLFilter();
        // Assuming .exe is filtered
        assertFalse(filter.isAllowed("http://test.com/download/file.exe"));
    }

    @Test
    public void testComplexQueryString() {
        FastURLFilter filter = new FastURLFilter();
        assertTrue(filter.isAllowed("http://somedomain.com/page?search=stormcrawler&sort=desc"));
    }
}