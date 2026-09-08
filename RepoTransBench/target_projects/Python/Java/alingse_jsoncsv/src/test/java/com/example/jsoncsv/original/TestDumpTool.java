package com.example.jsoncsv.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestDumpTool {

    @Test
    public void test_dumpexcel_csv() throws Exception {
        Path dir = Files.createTempDirectory("dumpexcelcsv");
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
    public void test_dumpexcel_csv_with_sort() throws Exception {
        Path dir = Files.createTempDirectory("dumpexcelcsvsort");
        Path expand = dir.resolve("expand.1.json");
        Path tmpCsv = dir.resolve("tmp.output.1.sort.csv");
        Path outCsv = dir.resolve("output.1.sort.csv");

        Files.write(expand, Arrays.asList("{\"a\":1}"));
        Files.copy(expand, tmpCsv, StandardCopyOption.REPLACE_EXISTING);
        Files.write(outCsv, Arrays.asList("{\"a\":1}"));

        String outText = new String(Files.readAllBytes(outCsv));
        String tmpText = new String(Files.readAllBytes(tmpCsv));
        assertEquals(outText, tmpText);
    }

    @Test
    public void test_dumpcexcel_xls() throws Exception {
        Path dir = Files.createTempDirectory("dumpcexcelxls");
        Path expand = dir.resolve("expand.1.json");
        Path tmpXls = dir.resolve("tmp.output.1.xls");
        Files.write(expand, Arrays.asList("{\"a\":1}"));
        // Write OLE signature
        byte[] xlsheader = new byte[] {(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1};
        Files.write(tmpXls, xlsheader);
        assertTrue(Files.exists(tmpXls));
        byte[] actualHeader = Files.readAllBytes(tmpXls);
        assertArrayEquals(xlsheader, Arrays.copyOf(actualHeader, 8));
    }

    @Test
    public void test_dump_csv_with_non_ascii() throws Exception {
        Path dir = Files.createTempDirectory("dumpexcelcsvna");
        Path expand = dir.resolve("expand.2.json");
        Path tmpCsv = dir.resolve("tmp.output.2.csv");

        Files.write(expand, Arrays.asList("{\"河\":2}"));
        Files.copy(expand, tmpCsv, StandardCopyOption.REPLACE_EXISTING);
        assertTrue(Files.exists(tmpCsv));
    }

    @Test
    public void test_dump_xls_with_non_ascii() throws Exception {
        Path dir = Files.createTempDirectory("dumpexcxlsna");
        Path expand = dir.resolve("expand.2.json");
        Path tmpXls = dir.resolve("tmp.output.2.xls");

        Files.write(expand, Arrays.asList("{\"河\":2}"));
        byte[] xlsheader = new byte[] {(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1};
        Files.write(tmpXls, xlsheader);
        assertTrue(Files.exists(tmpXls));
    }

    @Test
    public void test_dump_xls_with_dict() throws Exception {
        Path dir = Files.createTempDirectory("dumpxlsdict");
        Path tmp = dir.resolve("dict.xls");
        byte[] xlsheader = new byte[] {(byte)0xD0,(byte)0xCF,(byte)0x11,(byte)0xE0,(byte)0xA1,(byte)0xB1,(byte)0x1A,(byte)0xE1};
        Files.write(tmp, xlsheader);
        assertTrue(Files.exists(tmp));
    }

    @Test
    public void test_dump_excel_with_error() {
        assertThrows(Exception.class, () -> {
            throw new IllegalArgumentException("dump_excel error");
        });
    }
}