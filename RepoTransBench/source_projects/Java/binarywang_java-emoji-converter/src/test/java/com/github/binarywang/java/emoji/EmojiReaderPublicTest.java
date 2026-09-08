package com.github.binarywang.java.emoji;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class EmojiReaderPublicTest {
    @Test
    void testReadFromLocalPublic() {
        EmojiReader reader = new EmojiReader();
        assertNotNull(reader.read(true));
    }

    @Test
    void testSb2UnicodeMapNotNullPublic() {
        EmojiReader reader = new EmojiReader();
        assertNotNull(reader.getSb2UnicodeMap());
    }
}