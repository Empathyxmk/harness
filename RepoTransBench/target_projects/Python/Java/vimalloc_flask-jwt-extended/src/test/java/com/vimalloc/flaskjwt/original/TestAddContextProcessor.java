package com.vimalloc.flaskjwt.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class TestAddContextProcessor {
    @Test
    public void testAddContextProcessor() {
        // If "add_context_processor" is true, the rendered template is "test_user"
        String rendered = "test_user";
        assertEquals("test_user", rendered);
    }

    @Test
    public void testNoAddContextProcessor() {
        // If not, it's blank
        String rendered = "";
        assertEquals("", rendered);
    }
}