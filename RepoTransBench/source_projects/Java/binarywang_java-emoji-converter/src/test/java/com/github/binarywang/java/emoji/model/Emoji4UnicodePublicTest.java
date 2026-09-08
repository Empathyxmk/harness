package com.github.binarywang.java.emoji.model;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class Emoji4UnicodePublicTest {
    @Test
    public void testEmoji4UnicodePublicSettersAndGetters() {
        Emoji4Unicode unicode = new Emoji4Unicode();
        unicode.setCategories(null);
        assertNull(unicode.getCategories());
    }
}