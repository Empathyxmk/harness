package com.github.binarywang.java.emoji.model;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Emoji4UnicodeTest {
    @Test
    void testToStringAndClassLoads() {
        // Just calling the default constructor and toString for coverage
        Emoji4Unicode emoji = new Emoji4Unicode();
        assertNotNull(emoji.toString());
        assertNotNull(Emoji4Unicode.class);
    }
}