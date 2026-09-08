package com.onefilellm.original;

// Imports from the test_all.py suite converted to Java + JUnit 5/Mockito style

import com.onefilellm.utils.Utils;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

class TestAll {

    private Path tempDir;

    @BeforeEach
    void setUp() throws IOException {
        tempDir = Files.createTempDirectory("testdir");
    }

    @AfterEach
    void tearDown() throws IOException {
        if (tempDir != null) {
            Files.walk(tempDir)
                .sorted((a, b) -> b.compareTo(a))
                .forEach(path -> path.toFile().delete());
        }
    }

    @Test
    void testSafeFileRead() throws IOException {
        Path utf8File = tempDir.resolve("utf8.txt");
        Files.writeString(utf8File, "Hello 世界", StandardCharsets.UTF_8);
        assertEquals("Hello 世界", Utils.safeFileRead(utf8File.toString()));

        Path latin1File = tempDir.resolve("latin1.txt");
        Files.write(latin1File, "Café".getBytes("ISO-8859-1"));
        assertEquals("Café", Utils.safeFileRead(latin1File.toString()));
    }

    @Test
    void testFileExtensionDetection() {
        assertEquals(".py", Utils.getFileExtension("test.py"));
        assertEquals(".py", Utils.getFileExtension("TEST.PY"));
        assertEquals("", Utils.getFileExtension("no_extension"));
        assertEquals(".txt", Utils.getFileExtension("multiple.dots.txt"));
    }

    @Test
    void testIsBinaryFile() throws IOException {
        Path textFile = tempDir.resolve("text.txt");
        Files.writeString(textFile, "This is text", StandardCharsets.UTF_8);
        assertFalse(Utils.isBinaryFile(textFile.toString()));

        Path binaryFile = tempDir.resolve("binary.bin");
        Files.write(binaryFile, new byte[] {0, 1, 2, 3});
        assertTrue(Utils.isBinaryFile(binaryFile.toString()));
    }

    @Test
    void testIsExcludedFile() {
        assertTrue(Utils.isExcludedFile("test.pb.go"));
        assertTrue(Utils.isExcludedFile("file_test.go"));
        assertTrue(Utils.isExcludedFile("script.min.js"));
        assertTrue(Utils.isExcludedFile("__pycache__/file.pyc"));
        assertTrue(Utils.isExcludedFile("node_modules/package.json"));
        assertFalse(Utils.isExcludedFile("main.go"));
        assertFalse(Utils.isExcludedFile("app.js"));
    }

    @Test
    void testIsAllowedFiletype() {
        assertTrue(Utils.isAllowedFiletype("script.py"));
        assertTrue(Utils.isAllowedFiletype("README.md"));
        assertTrue(Utils.isAllowedFiletype("config.yaml"));
        assertFalse(Utils.isAllowedFiletype("image.png"));
        assertFalse(Utils.isAllowedFiletype("binary.exe"));
        assertFalse(Utils.isAllowedFiletype("archive.zip"));
    }

    @Test
    void testUrlUtilities() {
        String baseUrl = "https://example.com/docs/";
        assertTrue(Utils.isSameDomain(baseUrl, "https://example.com/other/"));
        assertFalse(Utils.isSameDomain(baseUrl, "https://other.com/docs/"));
        assertTrue(Utils.isWithinDepth(baseUrl, "https://example.com/docs/page1", 1));
        assertTrue(Utils.isWithinDepth(baseUrl, "https://example.com/docs/sub/page", 2));
        assertFalse(Utils.isWithinDepth(baseUrl, "https://example.com/docs/a/b/c", 2));
    }

    @Test
    void testEscapeXml() {
        String text = "<tag>Content & more</tag>";
        assertEquals(text, Utils.escapeXml(text));
    }

    // For the rest of the consolidated test_all.py, follow the same translation style:
    //  - Test format detection
    //  - Test stream processing (stdin/clipboard)
    //  - Test core processing functions
    //  - Test alias system behaviors (with temporary directories)
    //  - Test simulated integration with external systems
    //  - Test CLI and error handling
    //  - Test performance and large file handling

    // For lengthy test classes/categories, consider further splitting/organizing in auxiliary classes if the Java test suite grows large.

    // This class here demonstrates the complete logic for the first batch of such tests, with the rest to be fleshed out in similar structure.
}