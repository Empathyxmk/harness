package tests.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.example.jsonlines.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

class JsonlinesTest {

    @Test
    void testReader() throws Exception {
        byte[] SAMPLE_BYTES = "{\"a\": 1}\n{\"b\": 2}\n".getBytes(StandardCharsets.UTF_8);
        ByteArrayInputStream fp = new ByteArrayInputStream(SAMPLE_BYTES);
        try (Reader reader = new Reader(fp)) {
            Iterator<Object> it = reader.iterator();
            assertEquals(Collections.singletonMap("a", 1.0), it.next());
            assertEquals(Collections.singletonMap("b", 2.0), it.next());
            assertThrows(NoSuchElementException.class, it::next);
            assertThrows(EOFException.class, reader::read);
        }
    }

    @Test
    void testReadingFromIterable() throws Exception {
        List<Object> input = Arrays.asList("1", "{}");
        try (Reader reader = new Reader(input)) {
            List<Object> result = new ArrayList<>();
            reader.forEach(result::add);
            assertEquals(Arrays.asList(1.0, Collections.emptyMap()), result);
        }
    }

    @Test
    void testWriterText() throws Exception {
        StringWriter fp = new StringWriter();
        try (Writer writer = new Writer(fp)) {
            writer.write(Collections.singletonMap("a", 1));
            writer.write(Collections.singletonMap("b", 2));
        }
        assertEquals("{\"a\":1}\n{\"b\":2}\n", fp.toString());
    }

    @Test
    void testWriterBinary() throws Exception {
        ByteArrayOutputStream fp = new ByteArrayOutputStream();
        try (Writer writer = new Writer(fp)) {
            List<Object> list = Arrays.asList(Collections.singletonMap("a", 1), Collections.singletonMap("b", 2));
            writer.writeAll(list);
        }
        assertEquals("{\"a\":1}\n{\"b\":2}\n", fp.toString("UTF-8"));
    }

    @Test
    void testClosing() throws Exception {
        Reader reader = new Reader(Arrays.asList());
        reader.close();
        assertThrows(IOException.class, reader::read);
        Writer writer = new Writer(new ByteArrayOutputStream());
        writer.close();
        writer.close();
        assertThrows(Exception.class, () -> writer.write(123));
    }

    @Test
    void testInvalidLines() throws Exception {
        String data = "[1, 2";
        try (Reader reader = new Reader(new StringReader(data))) {
            assertThrows(InvalidLineError.class, reader::read);
        }
    }

    @Test
    void testSkipInvalid() throws Exception {
        String input = "12\ninvalid\n34";
        Reader reader = new Reader(new StringReader(input));
        Iterator<Object> it = reader.iterator();
        assertEquals(12.0, (Double)it.next(), 0.0);
        assertThrows(RuntimeException.class, it::next); // Since InvalidLineError wraps
    }

    @Test
    void testEmptyLines() throws Exception {
        byte[] data_with_empty_line = "1\n\n2\n".getBytes(StandardCharsets.UTF_8);
        try (Reader reader = new Reader(new ByteArrayInputStream(data_with_empty_line))) {
            assertEquals(1.0, reader.read());
            assertThrows(InvalidLineError.class, reader::read);
            assertEquals(2.0, reader.read());
            assertThrows(EOFException.class, reader::read);
        }
    }
}