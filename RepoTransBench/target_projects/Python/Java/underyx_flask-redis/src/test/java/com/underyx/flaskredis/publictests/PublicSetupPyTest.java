package com.underyx.flaskredis.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.regex.*;

class PublicSetupPyTest {

    private static String read(Path dir, String... paths) throws IOException {
        Path file = dir.toAbsolutePath();
        for (String p : paths) {
            file = file.resolve(p);
        }
        return Files.readString(file);
    }

    @Test
    void testReadReadsFilePublic() throws IOException {
        String testText = "123xyz";
        Path tmpDir = Files.createTempDirectory("testrf2");
        Path pkgDir = tmpDir.resolve("flask_redis");
        Files.createDirectory(pkgDir);
        Path filePath = pkgDir.resolve("testfile_public.txt");
        Files.writeString(filePath, testText);

        String result = read(tmpDir, "flask_redis", "testfile_public.txt");
        assertEquals(testText, result);

        try { Files.delete(filePath); } catch (Exception ignored) {}
        try { Files.delete(pkgDir); } catch (Exception ignored) {}
        try { Files.delete(tmpDir); } catch (Exception ignored) {}
    }

    private static String mockReadMeta(String metaString, String metaKey) {
        Pattern p = Pattern.compile("__" + Pattern.quote(metaKey) +
                "__\\s*=\\s*['\\\"]([^'\\\"]*)['\\\"]");
        Matcher m = p.matcher(metaString);
        if (m.find()) {
            return m.group(1);
        }
        throw new RuntimeException(String.format("Unable to find __%s__ string.", metaKey));
    }

    @Test
    void testFindMetaSuccessPublic() {
        String metaContent = "__spam__ = 'eggs'\n__hamp__ = 'bacon'";
        String result1 = mockReadMeta(metaContent, "spam");
        String result2 = mockReadMeta(metaContent, "hamp");
        assertEquals("eggs", result1);
        assertEquals("bacon", result2);
    }

    @Test
    void testFindMetaFailurePublic() {
        String metaContent = "";
        Exception exception = assertThrows(RuntimeException.class, () -> {
            mockReadMeta(metaContent, "somethingelse");
        });
        assertTrue(exception.getMessage().contains("Unable to find"));
    }
}