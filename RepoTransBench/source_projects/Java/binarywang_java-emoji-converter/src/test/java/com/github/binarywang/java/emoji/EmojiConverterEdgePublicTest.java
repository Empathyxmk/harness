package com.github.binarywang.java.emoji;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class EmojiConverterEdgePublicTest {
    @Test
    void testNullInputToAliasPublic() {
        EmojiConverter converter = EmojiConverter.getInstance();
        // Accept NPEs as expected, or test for actual behavior seen
        try {
            converter.toAlias(null);
            fail("Expected NullPointerException");
        } catch (NullPointerException e) {
            // expected
        }
    }

    @Test
    void testNullInputToUnicodePublic() {
        EmojiConverter converter = EmojiConverter.getInstance();
        try {
            converter.toUnicode(null);
            fail("Expected NullPointerException");
        } catch (NullPointerException e) {
            // expected
        }
    }

    @Test
    void testWhitespaceString() {
        EmojiConverter converter = EmojiConverter.getInstance();
        assertEquals(" ", converter.toAlias(" "));
        assertEquals(" ", converter.toUnicode(" "));
    }
}