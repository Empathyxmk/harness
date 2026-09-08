package com.scrapycssselect.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicApiImportsTest {

    @Test
    void testPublicApiImports() {
        try {
            Class.forName("com.scrapycssselect.cssselect.CssSelector");
            Class.forName("com.scrapycssselect.cssselect.ExpressionError");
        } catch (ClassNotFoundException e) {
            fail("API class not found: " + e.getMessage());
        }
    }
}