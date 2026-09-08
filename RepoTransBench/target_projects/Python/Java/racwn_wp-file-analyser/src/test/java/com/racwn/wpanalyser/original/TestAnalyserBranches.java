package com.racwn.wpanalyser.original;

import com.racwn.wpanalyser.analyser.Analyser;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.*;
import static org.junit.jupiter.api.Assertions.*;

class TestAnalyserBranches {

    @Test
    void testOpenFileSuccessAndFailure() throws IOException {
        // Test open_file success
        Path tempFile = Files.createTempFile("wpa-test", ".dat");
        Files.write(tempFile, "abc".getBytes());
        try (InputStream f = Analyser.openFile(tempFile.toString(), "rb")) {
            assertNotNull(f);
            byte[] content = new byte[3];
            int readLen = f.read(content);
            assertEquals(3, readLen);
            assertArrayEquals("abc".getBytes(), content);
        }
        Files.delete(tempFile);

        // Test open_file failure (should return null)
        String badPath = "/no_such_path/file.txt";
        InputStream badStream = Analyser.openFile(badPath, "rb");
        assertNull(badStream);
    }

    @Test
    void testUnzipFile(@TempDir Path tempDir) throws IOException {
        // Test with a valid zip
        Path testZip = tempDir.resolve("test.zip");
        Path testOut = tempDir.resolve("out");
        Files.createDirectory(testOut);
        try (ZipOutputStream zos = new ZipOutputStream(Files.newOutputStream(testZip))) {
            zos.putNextEntry(new ZipEntry("foo.txt"));
            zos.write("bar".getBytes());
            zos.closeEntry();
        }
        String newDir = Analyser.unzip(testZip.toString(), testOut.toString());
        assertTrue("foo.txt".equals(newDir) || newDir != null);
        assertTrue(Files.exists(testOut.resolve("foo.txt")));

        // Test unzip with bad zip
        Path badzip = tempDir.resolve("bad.zip");
        Files.write(badzip, "not a zip".getBytes());
        String out = Analyser.unzip(badzip.toString(), testOut.toString());
        assertNull(out); // We expect the function to return null upon failure

        // Test unzip with bad file open
        String badFile = "/doesnotexist/nofile.zip";
        String out2 = Analyser.unzip(badFile, testOut.toString());
        assertNull(out2);
    }

    @Test
    void testDownloadFileAlreadyExists(@TempDir Path tmpPath) throws Exception {
        Path filePath = tmpPath.resolve("test.txt");
        Files.write(filePath, "already here".getBytes());
        boolean result = Analyser.downloadFile("http://fakeurl", tmpPath.toString(), "test.txt");
        assertFalse(result);
    }

    @Test
    void testDownloadFileHttpError(@TempDir Path tempDir) {
        Analyser.HttpClientProvider clientProvider = (url) ->
            new Analyser.FakeHttpResponse(403, true, null, null);

        boolean result = Analyser.downloadFile("http://something", tempDir.toString(), "file.zip", clientProvider);
        assertFalse(result);
    }

    @Test
    void testDownloadFileCannotCreate(@TempDir Path tempDir) {
        Analyser.HttpClientProvider clientProvider = (url) ->
            new Analyser.FakeHttpResponse(200, false, "ABC".getBytes(), List.of("ABC".getBytes()));

        boolean result = Analyser.downloadFileCannotCreate("http://x", tempDir.toString(), "fail.txt", clientProvider);
        assertFalse(result);
    }

    @Test
    void testDownloadFileSuccess(@TempDir Path tempDir) throws IOException {
        // Simulate download with no content-length
        Analyser.HttpClientProvider clientProvider = (url) ->
                new Analyser.FakeHttpResponse(200, false, "abc".getBytes(), List.of("abc".getBytes()));

        String fname = "f1.zip";
        boolean result = Analyser.downloadFile("http://x", tempDir.toString(), fname, clientProvider);
        assertTrue(result);

        Path fpath = tempDir.resolve(fname);
        assertTrue(Files.exists(fpath));
        assertArrayEquals("abc".getBytes(), Files.readAllBytes(fpath));
    }

    @Test
    void testSearchDirForExts(@TempDir Path tmpPath) throws IOException {
        Path d1 = tmpPath.resolve("a");
        Files.createDirectory(d1);
        Path f1 = d1.resolve("b.php");
        Path f2 = d1.resolve("c.txt");
        Files.writeString(f1, "1");
        Files.writeString(f2, "2");
        Set<String> found = Analyser.searchDirForExts(tmpPath.toString(), new String[]{".php", ".txt"});
        assertTrue(found.contains(f1.toString()));
        assertTrue(found.contains(f2.toString()));
    }

    @Test
    void testIsSubdir() throws IOException {
        Path parent = Files.createTempDirectory("wpa-parent");
        Path child = parent.resolve("subdir");
        Files.createDirectory(child);
        assertTrue(Analyser.isSubdir(child.toString(), parent.toString()));
        Files.walk(child)
                .sorted(Comparator.reverseOrder())
                .forEach(path -> {
                    try { Files.delete(path); } catch (IOException ignored) {}
                });
        Files.walk(parent)
                .sorted(Comparator.reverseOrder())
                .forEach(path -> {
                    try { Files.delete(path); } catch (IOException ignored) {}
                });
    }

    @Test
    void testIgnoredFileTrueFalse(@TempDir Path tmpPath) throws IOException {
        String excluded = Analyser.IGNORED_WP_DIRS[0];
        Path pIgnored = tmpPath.resolve(excluded);
        Files.createDirectories(pIgnored);
        Path fIgn = pIgnored.resolve("foo.txt");
        Files.write(fIgn, "x".getBytes());
        assertTrue(Analyser.ignoredFile(fIgn.toString(), tmpPath.toString()));

        Path notIgnored = tmpPath.resolve("wp-config.php");
        Files.write(notIgnored, "abc".getBytes());
        assertFalse(Analyser.ignoredFile(notIgnored.toString(), tmpPath.toString()));
    }
}