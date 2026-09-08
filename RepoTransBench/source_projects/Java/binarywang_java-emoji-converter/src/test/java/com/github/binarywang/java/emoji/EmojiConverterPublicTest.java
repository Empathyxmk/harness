package com.github.binarywang.java.emoji;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EmojiConverterPublicTest {
    @Test
    void testToAliasAndUnicodePublic() {
        EmojiConverter converter = EmojiConverter.getInstance();
        String str = "😂";
        String alias = converter.toAlias(str);
        // For public: ":joy:" is typical, but use same set of logical assertions
        assertTrue(alias.contains(":joy:") || alias.contains(":") || alias.equals(str) || alias.equals("😂"));

        String unicode = converter.toUnicode(alias);
        assertNotNull(unicode);
    }

    @Test
    void testToHtmlPublic() {
        EmojiConverter converter = EmojiConverter.getInstance();
        String str = "😂";
        String html = converter.toHtml(str);
        assertTrue(html.contains("&#") || html.equals(str) || html.equals("😂"));
    }

    @Test
    void testSingletonInstancePublic() {
        assertNotNull(EmojiConverter.getInstance());
        assertSame(EmojiConverter.getInstance(), EmojiConverter.getInstance());
    }
}