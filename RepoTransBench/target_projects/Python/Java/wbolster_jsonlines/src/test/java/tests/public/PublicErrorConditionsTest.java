package tests.public;

import org.junit.jupiter.api.Test;

import com.example.jsonlines.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicErrorConditionsTest {

    @Test
    void testPublicInvalidRead() throws Exception {
        Path filePath = Files.createTempFile("pub_invalid1", ".txt");
        Files.write(filePath, "thisisnotjson\nnot-json-here\n".getBytes(StandardCharsets.UTF_8));
        try (Reader reader = new Reader(Files.newInputStream(filePath))) {
            assertThrows(Exception.class, () -> { List<Object> list = new ArrayList<>(); reader.forEach(list::add); });
        }
    }

    @Test
    void testPublicWriterToStream() throws Exception {
        Path filePath = Files.createTempFile("pub_stream", ".txt");
        try (Writer writer = new Writer(Files.newOutputStream(filePath))) {
            writer.write(Collections.singletonMap("out", "pubdata"));
        }
        byte[] raw = Files.readAllBytes(filePath);
        String rawStr = new String(raw, StandardCharsets.UTF_8);
        assertTrue(rawStr.contains("\"out\":\"pubdata\""));
    }
}