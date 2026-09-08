package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class HttpTest {

    @Test
    void testHttpApi() {
        // Just basic method call coverage, as actual network not tested
        try {
            assertTrue(Http.toUrl("http://example.com").contains("example"));
        } catch (Exception e) {
            fail(e);
        }
        assertEquals("GET", Http.methodType("GET"));

        assertNotNull(Http.agent());
        assertNotNull(Http.toStringOrNull(null));
        assertNull(Http.toStringOrNull(null));
    }
}