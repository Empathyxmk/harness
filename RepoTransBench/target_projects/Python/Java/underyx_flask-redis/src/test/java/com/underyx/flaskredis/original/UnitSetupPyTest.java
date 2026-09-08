package com.underyx.flaskredis.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.regex.*;
import java.util.*;

class UnitSetupPyTest {

    private static String read(Path dir, String... paths) throws IOException {
        // Simulates the Python "read(*paths)"
        Path file = dir.toAbsolutePath();
        for (String p : paths) {
            file = file.resolve(p);
        }
        return Files.readString(file);
    }

    @Test
    void testReadReadsFile() throws IOException {
        String testText = "abc";
        Path tmpDir = Files.createTempDirectory("testrf1");
        Path pkgDir = tmpDir.resolve("flask_redis");
        Files.createDirectory(pkgDir);
        Path filePath = pkgDir.resolve("dummy.py");
        Files.writeString(filePath, testText);

        String result = read(tmpDir, "flask_redis", "dummy.py");
        assertEquals(testText, result);

        // Cleanup
        try { Files.delete(filePath); } catch (Exception ignored) {}
        try { Files.delete(pkgDir); } catch (Exception ignored) {}
        try { Files.delete(tmpDir); } catch (Exception ignored) {}
    }

    private static String mockReadMeta(String metaString, String metaKey) {
        // Returns value of __metaKey__ = 'value'
        Pattern p = Pattern.compile("__" + Pattern.quote(metaKey) +
                "__\\s*=\\s*['\\\"]([^'\\\"]*)['\\\"]");
        Matcher m = p.matcher(metaString);
        if (m.find()) {
            return m.group(1);
        }
        throw new RuntimeException(String.format("Unable to find __%s__ string.", metaKey));
    }

    @Test
    void testFindMetaSuccess() {
        String metaContent = "__title__ = 'foo'\n__description__ = 'bar'";
        String result1 = mockReadMeta(metaContent, "title");
        String result2 = mockReadMeta(metaContent, "description");
        assertEquals("foo", result1);
        assertEquals("bar", result2);
    }

    @Test
    void testFindMetaFailure() {
        String metaContent = "";
        Exception exception = assertThrows(RuntimeException.class, () -> {
            mockReadMeta(metaContent, "whatever");
        });
        assertTrue(exception.getMessage().contains("Unable to find"));
    }
}