package tests.public;

import org.junit.jupiter.api.Test;

import com.example.jsonlines.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicJsonlinesTest {

    @Test
    void testPublicReader() throws Exception {
        byte[] sampleBytes = "{\"public\": 100}\n{\"nested\": {\"p\": 3}}\n".getBytes(StandardCharsets.UTF_8);
        ByteArrayInputStream fp = new ByteArrayInputStream(sampleBytes);
        try (Reader reader = new Reader(fp)) {
            Iterator<Object> it = reader.iterator();
            Map<String, Object> expected1 = new HashMap<>();
            expected1.put("public", 100.0);
            Map<String, Object> expected2 = new HashMap<>();
            Map<String, Object> nested = new HashMap<>();
            nested.put("p", 3.0);
            expected2.put("nested", nested);
            assertEquals(expected1, it.next());
            assertEquals(expected2, it.next());
            assertThrows(NoSuchElementException.class, it::next);
            assertThrows(EOFException.class, reader::read);
        }
    }

    @Test
    void testPublicWriterText() throws Exception {
        StringWriter fp = new StringWriter();
        try (Writer writer = new Writer(fp)) {
            writer.write(Collections.singletonMap("pubAlpha", 111));
            writer.write(Collections.singletonMap("pubBeta", 222));
        }
        assertEquals("{\"pubAlpha\":111}\n{\"pubBeta\":222}\n", fp.toString().replaceAll(" ", ""));
    }
}