package com.whonore.coqtail.original;

import org.junit.jupiter.api.Test;
import com.whonore.coqtail.xml.XMLInterface;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;

public class TestXMLInterface {

    @Test
    void testEscapeXMLSymbol() {
        String input = "apples & bananas < oranges > \"g\"";
        String result = XMLInterface.escape(input);
        assertTrue(result.contains("&amp;"));
        assertTrue(result.contains("&lt;"));
        assertTrue(result.contains("&gt;"));
        assertTrue(result.contains("&quot;"));
    }

    @Test
    void testUnescapeXMLSymbol() {
        String s = "&amp;hello&gt;&lt;test&gt;&quot;x&quot;";
        String result = XMLInterface.unescape(s);
        assertTrue(result.contains("&"));
        assertTrue(result.contains(">"));
        assertTrue(result.contains("<"));
        assertTrue(result.contains("\""));
    }

    @Test
    void testMakeElemWithAttrs() {
        HashMap<String, String> attrs = new HashMap<>();
        attrs.put("ripe", "yes");
        attrs.put("color", "yellow");
        String elem = XMLInterface.elem("fruit", "banana & apple", attrs);
        assertTrue(elem.contains("fruit"));
        assertTrue(elem.contains("ripe"));
        assertTrue(elem.contains("&amp;"));
    }
}