package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class ChineseWordPublicTest {

    @Test
    void testChineseWordWithOtherCharacters() {
        // Using different Chinese characters for a public test ("我们" meaning "we")
        me.zbl.composite.Character c1 = new me.zbl.composite.Character('我');
        me.zbl.composite.Character c2 = new me.zbl.composite.Character('们');
        ChineseWord word = new ChineseWord(Arrays.asList(c1, c2));
        assertEquals(2, word.count());
    }
}