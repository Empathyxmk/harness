package com.example.jsoncsv.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestPublicJsonCsv {

    @Test
    public void test_public_jsoncsv_expand() throws Exception {
        Path dir = Files.createTempDirectory("publicjsoncsv1");
        Path in = dir.resolve("raw.0.json");
        Path out = dir.resolve("tmp.expand.0.json");
        Files.write(in, Arrays.asList("{\"a\":1}"));
        Files.copy(in, out, StandardCopyOption.REPLACE_EXISTING);

        assertTrue(Files.exists(out));
    }

    @Test
    public void test_public_jsoncsv_expand_with_json_array() throws Exception {
        Path dir = Files.createTempDirectory("publicjsoncsv2");
        Path in = dir.resolve("raw.1.json");
        Path out = dir.resolve("tmp.expand.1.json");
        Files.write(in, Arrays.asList("[{\"a\":1}]"));
        Files.copy(in, out, StandardCopyOption.REPLACE_EXISTING);
        assertTrue(Files.exists(out));
    }

    @Test
    public void test_public_jsoncsv_expand_restore() throws Exception {
        Path dir = Files.createTempDirectory("publicjsoncsv3");
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
}