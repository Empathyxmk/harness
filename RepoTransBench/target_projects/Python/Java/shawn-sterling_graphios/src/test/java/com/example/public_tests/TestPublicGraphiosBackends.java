package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.example.graphios_backends.Utils;

public class TestPublicGraphiosBackends {

    @Test
    public void testPublicStripForbiddenChars() {
        assertEquals("abcdefg", Utils.strip_forbidden_chars("a/b:c*d?e<f>g|h"));
    }

    @Test
    public void testPublicStripAndLower() {
        assertEquals("abc-def_123", Utils.strip_and_lower("AbC-DeF_123"));
    }

    @Test
    public void testPublicStringCleanup() {
        assertEquals("Remove Spaces", Utils.string_cleanup("   Remove   Spaces   "));
    }

    @Test
    public void testPublicStringCleanupReplaces() {
        assertEquals("strip it now", Utils.string_cleanup("strip\tit   now"));
    }

    @Test
    public void testPublicCamelCaseToUnderscore() {
        assertEquals("public_case_to_underscore", Utils.camel_case_to_underscore("PublicCaseToUnderscore"));
    }

    @Test
    public void testPublicStripUnicode() {
        String text = "café 漢字";
        String result = Utils.strip_unicode(text);
        assertTrue(result.contains("cafe"));
        for (char c : result.toCharArray()) {
            assertTrue((int)c < 128);
        }
    }

    @Test
    public void testPublicGetattrFromPath() {
        Object res = Utils.getattr_from_path("dummy_mod.Dummy.Inner.value");
        assertEquals(404, res);
    }
}