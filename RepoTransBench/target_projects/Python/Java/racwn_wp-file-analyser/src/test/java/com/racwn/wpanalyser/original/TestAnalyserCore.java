package com.racwn.wpanalyser.original;

import com.racwn.wpanalyser.analyser.Analyser;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.*;

import static org.junit.jupiter.api.Assertions.*;

class TestAnalyserCore {

    @Test
    void testMsgVerbosePrints() {
        PrintStream origOut = System.out;
        ByteArrayOutputStream bout = new ByteArrayOutputStream();
        System.setOut(new PrintStream(bout));
        try {
            Analyser.setVerbose(true);
            Analyser.msg("hello!", false);
            String output = bout.toString();
            assertTrue(output.contains("hello!"));
        } finally {
            System.setOut(origOut);
        }
    }

    @Test
    void testMsgErrorPrints() {
        PrintStream origOut = System.out;
        ByteArrayOutputStream bout = new ByteArrayOutputStream();
        System.setOut(new PrintStream(bout));
        try {
            Analyser.setVerbose(false);
            Analyser.msg("error happened", true);
            String output = bout.toString();
            assertTrue(output.contains("error happened"));
        } finally {
            System.setOut(origOut);
        }
    }

    @Test
    void testMsgNotVerbose() {
        PrintStream origOut = System.out;
        ByteArrayOutputStream bout = new ByteArrayOutputStream();
        System.setOut(new PrintStream(bout));
        try {
            Analyser.setVerbose(false);
            Analyser.msg("no print", false);
            String output = bout.toString();
            assertEquals("", output);
        } finally {
            System.setOut(origOut);
        }
    }

    @Test
    void testOpenFileSuccess(@TempDir Path tmpPath) throws IOException {
        Path fPath = tmpPath.resolve("a.txt");
        Files.writeString(fPath, "abc");
        Reader f = Analyser.openFileForRead(fPath.toString());
        assertNotNull(f);
        String text = new BufferedReader(f).readLine();
        assertTrue(text.contains("abc"));
        f.close();
    }

    @Test
    void testOpenFileFail() {
        Reader f = Analyser.openFileForRead("notfound.txt");
        assertNull(f);
    }

    @Test
    void testUnzipSuccess(@TempDir Path tmpPath) throws IOException {
        Path tmpZip = tmpPath.resolve("t1.zip");
        Path extractDir = tmpPath.resolve("extr");
        Files.createDirectory(extractDir);
        String fileInZip = "dirA/file.txt";
        byte[] fileContent = "hi zip".getBytes();
        try (ZipOutputStream zos = new ZipOutputStream(Files.newOutputStream(tmpZip))) {
            zos.putNextEntry(new ZipEntry(fileInZip));
            zos.write(fileContent);
            zos.closeEntry();
        }
        String toplevel = Analyser.unzip(tmpZip.toString(), extractDir.toString());
        assertTrue(toplevel.contains("dirA") || toplevel.equals("dirA/file.txt"));
        assertTrue(Files.exists(extractDir.resolve(fileInZip)));
    }

    @Test
    void testUnzipRuntimeError(@TempDir Path tmpPath) throws IOException {
        Path zf = tmpPath.resolve("a.zip");
        Files.write(zf, "fakedata".getBytes());
        String result = Analyser.unzipRuntimeError(zf.toString(), tmpPath.toString());
        assertNull(result);
    }

    @Test
    void testUnzipBadZip(@TempDir Path tmpPath) throws IOException {
        Path zf = tmpPath.resolve("notzip.zip");
        Files.write(zf, "fakedata".getBytes());
        String result = Analyser.unzipBadZip(zf.toString(), tmpPath.toString());
        assertNull(result);
    }

    @Test
    void testUnzipIOError(@TempDir Path tmpPath) throws IOException {
        Path zf = tmpPath.resolve("notzip2.zip");
        Files.write(zf, "fake2".getBytes());
        String result = Analyser.unzipIoError(zf.toString(), tmpPath.toString());
        assertNull(result);
    }

    @Test
    void testSearchDirForExts(@TempDir Path tmpPath) throws IOException {
        Path aPhp = tmpPath.resolve("a.php");
        Path bTxt = tmpPath.resolve("b.txt");
        Path dir = tmpPath.resolve("dir");
        Files.createDirectory(dir);
        Path cPhtml = dir.resolve("c.phtml");
        Files.writeString(aPhp, "<?php ?>");
        Files.writeString(bTxt, "hi");
        Files.writeString(cPhtml, "<?php ?>");
        Set<String> found = Analyser.searchDirForExts(tmpPath.toString(), new String[]{".php", ".phtml"});
        Set<String> basenames = new HashSet<>();
        for (String s : found) basenames.add(Paths.get(s).getFileName().toString());
        assertTrue(basenames.contains("a.php"));
        assertTrue(basenames.contains("c.phtml"));
        assertFalse(basenames.contains("b.txt"));
    }

    @Test
    void testIsSubdirTrue(@TempDir Path tmpPath) throws IOException {
        Path sub = tmpPath.resolve("out");
        Files.createDirectory(sub);
        assertTrue(Analyser.isSubdir(sub.toString(), tmpPath.toString()));
    }

    @Test
    void testIsSubdirFalse(@TempDir Path tmpPath) throws IOException {
        Path base = tmpPath.resolve("up");
        Path other = tmpPath.resolve("x");
        Files.createDirectory(base);
        Files.createDirectory(other);
        assertFalse(Analyser.isSubdir(base.toString(), other.toString()));
    }

    @Test
    void testDownloadFileFileExists(@TempDir Path tmpPath) throws IOException {
        Path f = tmpPath.resolve("exist.file");
        Files.writeString(f, "abc");
        boolean exists = Analyser.downloadFileFileExists("http://a", tmpPath.toString(), "exist.file");
        assertFalse(exists);
    }

    @Test
    void testDownloadFileSuccess(@TempDir Path tmpPath) throws IOException {
        Analyser.HttpClientProvider clientProvider = (url) ->
                new Analyser.FakeHttpResponse(200, false, "abc".getBytes(), List.of("abc".getBytes()));
        boolean ok = Analyser.downloadFile("http://fake", tmpPath.toString(), "af", clientProvider);
        assertTrue(ok);
        Path filePath = tmpPath.resolve("af");
        assertEquals("abc", Files.readString(filePath));
    }

    @Test
    void testDownloadFileResponseHttpError(@TempDir Path tmpPath) throws IOException {
        Analyser.HttpClientProvider clientProvider = (url) ->
                new Analyser.FakeHttpResponse(404, true, new byte[0], List.of());
        boolean ok = Analyser.downloadFile("http://fail.com", tmpPath.toString(), "af", clientProvider);
        assertFalse(ok);
    }

    @Test
    void testDownloadFileOpenFileFalse(@TempDir Path tmpPath) {
        boolean ok = Analyser.downloadFileOpenFileFalse("http://fail.com", tmpPath.toString(), "af");
        assertFalse(ok);
    }
}