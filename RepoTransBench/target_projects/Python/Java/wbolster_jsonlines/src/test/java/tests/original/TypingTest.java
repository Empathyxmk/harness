package tests.original;

import org.junit.jupiter.api.Test;

import com.example.jsonlines.*;

import java.io.*;

import static org.junit.jupiter.api.Assertions.*;

class TypingTest {
    @Test
    void testTypingWithReader() throws Exception {
        Reader reader = new Reader(new StringReader("\"typedText\""));
        Object result = reader.read();
        assertEquals("typedText", result);
    }

    @Test
    void testTypingWithWriter() throws Exception {
        StringWriter sw = new StringWriter();
        Writer writer = new Writer(sw);
        writer.write("banana");
        writer.close();
        assertTrue(sw.toString().contains("banana"));
    }

    @Test
    void testTypingWithOpen() throws Exception {
        File tempf = File.createTempFile("testTypingOpen", ".jsonl");
        tempf.deleteOnExit();
        Writer writer = new Writer(new FileWriter(tempf));
        writer.write("bazquux");
        writer.close();
        Reader reader = new Reader(new FileReader(tempf));
        Object obj = reader.read();
        assertEquals("bazquux", obj);
        reader.close();
    }
}