package com.powergo.pytracking.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class TestHtml {

    @Test
    void testHtmlEscaping() {
        String s = "<div class='test'>& \"</div>";
        // Equivalent of Python's html.escape(s, quote=True)
        String expected = "&lt;div class=&#39;test&#39;&gt;&amp; &quot;&lt;/div&gt;";
        String escaped = s.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                        .replace("\"", "&quot;")
                        .replace("'", "&#39;");
        assertEquals(expected, escaped);
    }

    @Test
    void testHtmlUnescaping() {
        String escaped = "&lt;tag&gt;Test &amp; &quot;escaped&quot;&lt;/tag&gt;";
        // Unescape basic common HTML
        String unescaped = escaped
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", "\"")
            .replace("&#39;", "'");
        assertEquals("<tag>Test & \"escaped\"</tag>", unescaped);
    }

    @Test
    void testUrlEncoding() {
        String s = "a=b&c=d e/";
        String encoded = URLEncoder.encode(s, StandardCharsets.UTF_8);
        // Python's urllib.parse.quote("a=b&c=d e/") = 'a%3Db%26c%3Dd%20e%2F'
        assertEquals("a%3Db%26c%3Dd+e%2F", encoded); // Java uses + for space
    }
}