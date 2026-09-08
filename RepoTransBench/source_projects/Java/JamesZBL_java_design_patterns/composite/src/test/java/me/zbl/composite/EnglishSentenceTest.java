package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class EnglishSentenceTest {

    @Test
    void testConstructorAndPrintAfter() {
        EnglishWord word = new EnglishWord(Collections.emptyList());
        EnglishSentence sentence = new EnglishSentence(Collections.singletonList(word));
        assertEquals(1, sentence.count());
        // test printAfter() outputs a period newline
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));
        sentence.printAfter();
        System.setOut(System.out);
        assertEquals(".\n", out.toString().replace("\r\n", "\n")); // handle platform eol
    }
}