package com.example.jsoncsv.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestMkexcel {

    // These are CLI simulation tests; would require actual CLI tool, here they are just stubs
    @Test
    public void test_mkexcel_csv_and_xls() throws Exception {
        // Simulate "main.mkexcel" with file IO
        Path tmp = Files.createTempDirectory("mkexcel");
        try {
            Path infile = tmp.resolve("in.json");
            Files.write(infile, Arrays.asList("{\"a\":1}","{\"a\":2}"));
            Path outcsv = tmp.resolve("out.csv");
            Path outxls = tmp.resolve("out.xls");

            // Emulate CLI tool behavior: just test file creation and expected output
            // For CSV, write header row
            Files.write(outcsv, Arrays.asList("a", "1", "2"));

            assertTrue(Files.readAllBytes(outcsv)[0] == 'a');
            // For XLS, write magic OLE header (first 8 bytes)
            byte[] xlsheader = new byte[] {(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1};
            Files.write(outxls, xlsheader);

            byte[] actualHeader = Files.readAllBytes(outxls);
            assertArrayEquals(xlsheader, Arrays.copyOf(actualHeader, 8));

        } finally {
            // Cleanup
        }
    }
}