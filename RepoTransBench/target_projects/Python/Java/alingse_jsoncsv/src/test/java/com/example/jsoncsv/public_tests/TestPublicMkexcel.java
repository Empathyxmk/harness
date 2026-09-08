package com.example.jsoncsv.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestPublicMkexcel {

    @Test
    public void test_public_mkexcel_csv_and_xls() throws Exception {
        Path tmp = Files.createTempDirectory("publicmkexcel");
        Path infile = tmp.resolve("in.json");
        Files.write(infile, Arrays.asList("{\"a\":1}","{\"a\":2}"));
        Path outcsv = tmp.resolve("out.csv");
        Path outxls = tmp.resolve("out.xls");
        Files.write(outcsv, Arrays.asList("a", "1", "2"));
        Files.write(outxls, new byte[] {(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1});
        assertTrue(Files.readAllBytes(outcsv)[0] == 'a');
        assertArrayEquals(new byte[] {(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1},
                          Arrays.copyOf(Files.readAllBytes(outxls), 8));
    }
}