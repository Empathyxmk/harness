package com.example.mammoth.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class HtmlPathsModuleTest {
    @Test
    void testSimplePath() {
        HtmlPath path = new HtmlPath("p");
        assertEquals("<p></p>", path.toHtml());
    }

    @Test
    void testPathWithAttributes() {
        HtmlPath path = new HtmlPath("span", "class", "highlight");
        assertEquals("<span class=\"highlight\"></span>", path.toHtml());
    }

    static class HtmlPath {
        private final String tag;
        private final String attr;
        private final String value;
        HtmlPath(String tag) { this(tag, null, null); }
        HtmlPath(String tag, String attr, String value) {
            this.tag = tag;
            this.attr = attr;
            this.value = value;
        }
        String toHtml() {
            if (attr == null) return "<" + tag + "></" + tag + ">";
            return "<" + tag + " " + attr + "=\"" + value + "\"></" + tag + ">";
        }
    }
}