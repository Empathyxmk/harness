package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {

    // Simulating utility functions

    static class CheckAjax {
        static boolean isAjax(String header) {
            return "XMLHttpRequest".equals(header);
        }
    }

    @Test
    void testIsAjaxDetectsXmlHttpRequest() {
        assertTrue(CheckAjax.isAjax("XMLHttpRequest"));
        assertFalse(CheckAjax.isAjax("SomeOtherHeader"));
        assertFalse(CheckAjax.isAjax(null));
    }
}