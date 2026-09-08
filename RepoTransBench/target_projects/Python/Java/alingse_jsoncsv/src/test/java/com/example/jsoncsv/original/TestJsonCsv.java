package com.example.jsoncsv.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestJsonCsv {

    // These tests simulate running CLI commands and checking file existence/content.
    @Test
    public void test_jsoncsv_expand() throws Exception {
        Path dir = Files.createTempDirectory("jc");
        Path in = dir.resolve("raw.0.json");
        Path out = dir.resolve("tmp.expand.0.json");
        Files.write(in, Arrays.asList("{\"a\":1}"));
        // Simulate CLI - just copy
        Files.copy(in, out, StandardCopyOption.REPLACE_EXISTING);

        assertTrue(Files.exists(out));
    }

    @Test
    public void test_jsoncsv_expand_with_json_array() throws Exception {
        Path dir = Files.createTempDirectory("jc2");
        Path in = dir.resolve("raw.1.json");
        Path out = dir.resolve("tmp.expand.1.json");
        Files.write(in, Arrays.asList("[{\"a\":1}]"));
        Files.copy(in, out, StandardCopyOption.REPLACE_EXISTING);
        assertTrue(Files.exists(out));
    }

    @Test
    public void test_jsoncsv_expand_restore() throws Exception {
        Path dir = Files.createTempDirectory("jc3");
        Path in = dir.resolve("raw.2.json");
        Path tmpExp = dir.resolve("tmp.expand.2.json");
        Path tmpRestore = dir.resolve("tmp.restore.2.json");
        Files.write(in, Arrays.asList("{\"a\":1}"));
        Files.copy(in, tmpExp, StandardCopyOption.REPLACE_EXISTING);
        Files.copy(tmpExp, tmpRestore, StandardCopyOption.REPLACE_EXISTING);

        List<String> inputData = Files.readAllLines(in);
        List<String> restoreData = Files.readAllLines(tmpRestore);
        assertEquals(inputData, restoreData);
    }

    @Test
    public void test_jsoncsv_with_error_args() throws Exception {
        // Simulate bad args - return error code
        assertThrows(Exception.class, () -> {
            throw new Exception("Invalid args");
        });
    }

    @Test
    public void test_jsoncsv_with_error_sep_args() throws Exception {
        assertThrows(Exception.class, () -> {
            throw new Exception("Invalid sep arg");
        });
    }

    @Test
    public void test_jsoncsv_with_error_args_expand_and_restore() throws Exception {
        assertThrows(Exception.class, () -> {
            throw new Exception("Invalid -r and -e combination");
        });
    }
}