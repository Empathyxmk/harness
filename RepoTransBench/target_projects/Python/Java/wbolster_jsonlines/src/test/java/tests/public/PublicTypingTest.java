package tests.public;

import org.junit.jupiter.api.Test;

import com.example.jsonlines.*;

import java.io.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicTypingTest {
    @Test
    void testPublicTypingWithReader() throws Exception {
        Reader reader = new Reader(new StringReader("\"pubText\""));
        Object result = reader.read();
        assertEquals("pubText", result);
    }

    @Test
    void testPublicTypingWithWriter() throws Exception {
        StringWriter sw = new StringWriter();
        Writer writer = new Writer(sw);
        writer.write("PUB");
        writer.close();
        assertTrue(sw.toString().contains("PUB"));
    }

    @Test
    void testPublicTypingWithOpen() throws Exception {
        File tempf = File.createTempFile("publicTypingOpen", ".jsonl");
        tempf.deleteOnExit();
        Writer writer = new Writer(new FileWriter(tempf));
        writer.write("pubopen");
        writer.close();
        Reader reader = new Reader(new FileReader(tempf));
        Object obj = reader.read();
        assertEquals("pubopen", obj);
        reader.close();
    }
}