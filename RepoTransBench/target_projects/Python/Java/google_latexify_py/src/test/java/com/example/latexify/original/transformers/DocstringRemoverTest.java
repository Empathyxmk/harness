package com.example.latexify.original.transformers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DocstringRemoverTest {
    static String removeDocstring(String code) {
        // Remove triple-quoted string at start
        return code.replaceFirst("^\"\"\"[\\s\\S]*?\"\"\"", "").trim();
    }

    @Test
    void testRemoveDocstring() {
        assertEquals("def foo(): pass", removeDocstring("\"\"\"doc\"\"\"\ndef foo(): pass"));
        assertEquals("def bar(): pass", removeDocstring("\"\"\"\nlong\ndoc\n\"\"\"\ndef bar(): pass"));
    }

    @Test
    void testNoDocstring() {
        assertEquals("def baz(): pass", removeDocstring("def baz(): pass"));
    }
}