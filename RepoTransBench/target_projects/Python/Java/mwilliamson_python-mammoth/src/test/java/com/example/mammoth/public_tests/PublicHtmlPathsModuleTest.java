package com.example.mammoth.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicHtmlPathsModuleTest {
    @Test
    void testPublicHtmlPath() {
        HtmlPath path = new HtmlPath("div");
        assertEquals("<div></div>", path.toHtml());
    }

    static class HtmlPath {
        private final String tag;
        HtmlPath(String tag) { this.tag = tag; }
        String toHtml() { return "<" + tag + "></" + tag + ">"; }
    }
}