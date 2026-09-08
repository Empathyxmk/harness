package me.zbl.composite;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

class WriterIntegrationPublicTest {
    @Test
    void testWriterSentencesPublic() {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(baos));
        // Call only one sentence to test different output path
        new Writer().sentenceByEnglish().print();
        System.setOut(old);
        String result = baos.toString();
        // Ensure at least the result contains 'student' and a 'from'
        assert(result.contains("student"));
        assert(result.contains("from"));
    }
}