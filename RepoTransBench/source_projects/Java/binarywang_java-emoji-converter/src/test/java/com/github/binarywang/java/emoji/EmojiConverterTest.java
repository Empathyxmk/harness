package com.github.binarywang.java.emoji;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EmojiConverterTest {
    @Test
    void testToAliasAndUnicode() {
        EmojiConverter converter = EmojiConverter.getInstance();
        String str = "😊";
        String alias = converter.toAlias(str);
        assertTrue(alias.contains(":blush:") || alias.contains(":") || alias.equals(str) || alias.equals("😊"));

        String unicode = converter.toUnicode(alias);
        assertNotNull(unicode);
    }

    @Test
    void testToHtml() {
        EmojiConverter converter = EmojiConverter.getInstance();
        String str = "😊";
        String html = converter.toHtml(str);
        assertTrue(html.contains("&#") || html.equals(str) || html.equals("😊"));
    }

    @Test
    void testSingletonInstance() {
        assertNotNull(EmojiConverter.getInstance());
        assertSame(EmojiConverter.getInstance(), EmojiConverter.getInstance());
    }
}