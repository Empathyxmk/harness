package tests.original;

import org.junit.jupiter.api.Test;

import com.example.jsonlines.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class JsonlinesExtraTest {

    @Test
    void testDefaultDumpsNotImplemented() {
        assertThrows(RuntimeException.class, () -> com.example.jsonlines.JsonlinesUtil.defaultDumps(456));
    }

    @Test
    void testInvalidLineErrorProps() {
        InvalidLineError err = new InvalidLineError("Ohno", "badjson", 5);
        assertTrue(err instanceof Error);
        assertEquals("badjson", err.getLine());
        assertEquals(5, err.getLineno());
        assertTrue(err.toString().contains("Ohno"));
        InvalidLineError err2 = new InvalidLineError("OtherMsg", "newline\n", 3);
        assertEquals("newline", err2.getLine());
    }

    @Test
    void testReaderWriterBaseCloseMultiple() {
        ReaderWriterBase base = new ReaderWriterBase();
        base.close();
        base.close();
    }

    @Test
    void testReaderWriterBaseEq() {
        ReaderWriterBase base1 = new ReaderWriterBase();
        ReaderWriterBase base2 = new ReaderWriterBase();
        assertEquals(base1, base2);
    }

    @Test
    void testWriterSupportedTypes() throws Exception {
        Path path = Files.createTempFile("extra_test", ".jsonl");
        List<Object> data = Arrays.asList(
                Collections.singletonMap("bar", 88),
                Arrays.asList(2, 7),
                3,
                1.4,
                true,
                "hello"
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
    void testWriterWriteUnsupportedType() throws Exception {
        Path path = Files.createTempFile("extra_usertype", ".jsonl");
        class MyData {}
        try (Writer fileWriter = new Writer(Files.newBufferedWriter(path, StandardCharsets.UTF_8))) {
            assertThrows(Exception.class, () -> fileWriter.write(new MyData()));
        }
    }

}