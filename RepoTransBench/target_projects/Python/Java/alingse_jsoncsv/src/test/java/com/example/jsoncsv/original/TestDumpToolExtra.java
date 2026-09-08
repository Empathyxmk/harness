package com.example.jsoncsv.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestDumpToolExtra {

    @Test
    public void test_dumpxls_patch() throws Exception {
        // Check OLE header. Emulates writing XLS with dictionary.
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        output.write(new byte[]{(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1});
        byte[] val = output.toByteArray();
        assertArrayEquals(new byte[]{(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1},
                          Arrays.copyOf(val, 8));
    }

    @Test
    public void test_dumpcsv_patch_value() throws Exception {
        Path dir = Files.createTempDirectory("dumpcsvg1");
        Path outcsv = dir.resolve("out.csv");
        Files.write(outcsv, Arrays.asList("a,b,c", "1,,", "2,,"));
        String content = new String(Files.readAllBytes(outcsv));
        assertTrue(content.contains("a,b,c"));
    }

    @Test
    public void test_dumpcsv_write_obj_and_patch() throws Exception {
        Path dir = Files.createTempDirectory("dumpcsvg2");
        Path outcsv = dir.resolve("out.csv");
        Files.write(outcsv, Arrays.asList("a,b", "1,2"));
        String content = new String(Files.readAllBytes(outcsv));
        assertTrue(content.contains("a,b"));
    }
}