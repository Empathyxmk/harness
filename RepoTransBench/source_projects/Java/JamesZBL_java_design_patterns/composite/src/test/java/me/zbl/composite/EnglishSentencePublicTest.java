package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class EnglishSentencePublicTest {

    @Test
    void testSentenceCompositionPublic() {
        EnglishWord word1 = new EnglishWord(Arrays.asList(new Character('T'), new Character('e'), new Character('s'), new Character('t')));
        EnglishWord word2 = new EnglishWord(Arrays.asList(new Character('P'), new Character('u'), new Character('b'), new Character('l'), new Character('i'), new Character('c')));
        EnglishSentence s = new EnglishSentence(Arrays.asList(word1, word2));
        assertEquals(2, s.count());
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(baos));
        s.print();
        System.setOut(old);
        assertTrue(baos.toString().contains("."));
    }
}