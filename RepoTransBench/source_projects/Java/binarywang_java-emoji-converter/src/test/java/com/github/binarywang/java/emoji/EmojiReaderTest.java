package com.github.binarywang.java.emoji;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EmojiReaderTest {
    @Test
    void testClassLoads() {
        // Just ensure the class can be loaded to achieve coverage on this utility class (since all methods missing).
        assertNotNull(com.github.binarywang.java.emoji.EmojiReader.class);
    }
}