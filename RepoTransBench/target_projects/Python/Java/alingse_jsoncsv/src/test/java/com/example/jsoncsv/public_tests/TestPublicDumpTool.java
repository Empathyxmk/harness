package com.example.jsoncsv.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestPublicDumpTool {

    @Test
    public void test_public_dumpexcel_csv() throws Exception {
        Path dir = Files.createTempDirectory("publicdumpexcelcsv1");
        Path expand = dir.resolve("expand.1.json");
        Path tmpCsv = dir.resolve("tmp.output.1.csv");
        Path outCsv = dir.resolve("output.1.csv");

        Files.write(expand, Arrays.asList("{\"a\":1}"));
        Files.copy(expand, tmpCsv, StandardCopyOption.REPLACE_EXISTING);
        Files.write(outCsv, Arrays.asList("{\"a\":1}"));
        String outText = new String(Files.readAllBytes(outCsv));
        String tmpText = new String(Files.readAllBytes(tmpCsv));
        assertEquals(outText, tmpText);
    }

    @Test
    public void test_public_dumpcexcel_xls() throws Exception {
        Path dir = Files.createTempDirectory("publicdumpcexcelxls");
        Path expand = dir.resolve("expand.1.json");
        Path tmpXls = dir.resolve("tmp.output.1.xls");
        Files.write(expand, Arrays.asList("{\"a\":1}"));
        byte[] xlsheader = new byte[] {(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1};
        Files.write(tmpXls, xlsheader);
        assertTrue(Files.exists(tmpXls));
        byte[] actualHeader = Files.readAllBytes(tmpXls);
        assertArrayEquals(xlsheader, Arrays.copyOf(actualHeader, 8));
    }
}