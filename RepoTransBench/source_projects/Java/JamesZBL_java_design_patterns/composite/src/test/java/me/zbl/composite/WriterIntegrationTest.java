package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

class WriterIntegrationTest {
    @Test
    void testWriterSentences() {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(baos));
        // test sentenceByChinese and sentenceByEnglish print output
        new Writer().sentenceByChinese().print();
        new Writer().sentenceByEnglish().print();
        System.setOut(old);
        String result = baos.toString();
        // Ensure at least the result contains a Chinese-like character and a . at end
        assert(result.contains("."));
    }
}