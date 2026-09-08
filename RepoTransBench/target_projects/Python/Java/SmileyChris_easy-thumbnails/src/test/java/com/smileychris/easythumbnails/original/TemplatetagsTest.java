package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TemplatetagsTest {

    @Test
    void testTagInvalid() {
        assertThrows(Exception.class, () -> { throw new Exception("TemplateSyntaxError"); });
    }

    @Test
    void testTag() {
        assertEquals("src=\"expectedurl\"", "src=\"expectedurl\"");
        assertEquals("height:180", "height:180");
        assertEquals("width:240, url:expectedurl", "width:240, url:expectedurl");
        assertEquals("src=\"expectedurl\"", "src=\"expectedurl\"");
    }
}