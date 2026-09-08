package tests.public;

import org.junit.jupiter.api.Test;

import com.example.jsonlines.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicJsonlinesExtraTest {

    @Test
    void testPublicDefaultDumpsNotImplemented() {
        assertThrows(RuntimeException.class, () -> com.example.jsonlines.JsonlinesUtil.defaultDumps("testing"));
    }

    @Test
    void testPublicInvalidLineErrorProperties() {
        InvalidLineError err = new InvalidLineError("Oops", "publicbadjson", 8);
        assertTrue(err instanceof Error);
        assertEquals("publicbadjson", err.getLine());
        assertEquals(8, err.getLineno());
        assertTrue(err.toString().contains("Oops"));
        InvalidLineError err2 = new InvalidLineError("MsgPub", "lpublicagain\n", 2);
        assertEquals("lpublicagain", err2.getLine());
    }

    @Test
    void testPublicReaderWriterBaseCloseSeveral() {
        ReaderWriterBase base = new ReaderWriterBase();
        base.close();
        base.close();
        base.close();
    }

    @Test
    void testPublicReaderWriterBaseEquality() {
        ReaderWriterBase base1 = new ReaderWriterBase();
        ReaderWriterBase base2 = new ReaderWriterBase();
        assertEquals(base1, base2);
    }

    @Test
    void testPublicWriterWriteAllTypes() throws Exception {
        Path path = Files.createTempFile("public_more_test", ".jsonl");
        List<Object> data = Arrays.asList(
                Collections.singletonMap("key", 42),
                Arrays.asList(1, 0),
                42,
                0.42,
                true,
                "jsonl"
        );
        try (Writer fileWriter = new Writer(Files.newBufferedWriter(path, StandardCharsets.UTF_8))) {
            for (Object item : data) fileWriter.write(item);
        }
        List<Object> got;
        try (Reader reader = new Reader(Files.newBufferedReader(path, StandardCharsets.UTF_8))) {
            got = new ArrayList<>();
            reader.forEach(got::add);
        }
        assertEquals(data, got);
    }

    @Test
    void testPublicWriterWriteNonJsonable() throws Exception {
        Path path = Files.createTempFile("public_customtype", ".jsonl");
        class MyType {}
        try (Writer fileWriter = new Writer(Files.newBufferedWriter(path, StandardCharsets.UTF_8))) {
            assertThrows(Exception.class, () -> fileWriter.write(new MyType()));
        }
    }
}