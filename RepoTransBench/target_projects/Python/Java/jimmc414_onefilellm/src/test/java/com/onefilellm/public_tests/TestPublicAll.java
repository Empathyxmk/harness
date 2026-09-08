package com.onefilellm.public_tests;

import com.onefilellm.utils.Utils;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

class TestPublicAll {

    private Path tmpd;

    @BeforeEach
    void setUp() throws IOException {
        tmpd = Files.createTempDirectory("tempdata");
    }

    @AfterEach
    void tearDown() throws IOException {
        if (tmpd != null) {
            Files.walk(tmpd)
                    .sorted(Comparator.reverseOrder())
                    .map(Path::toFile)
                    .forEach(File::delete);
        }
    }

    @Test
    void testSafeFileReadPublic() throws IOException {
        Path fUtf8 = tmpd.resolve("abc.txt");
        String data = "Public 测试";
        Files.writeString(fUtf8, data, StandardCharsets.UTF_8);
        assertEquals(data, Utils.safeFileRead(fUtf8.toString()));

        Path fLatin1 = tmpd.resolve("latinpublic.txt");
        String latinText = "mañana";
        Files.write(fLatin1, latinText.getBytes("ISO-8859-1"));
        assertEquals(latinText, Utils.safeFileRead(fLatin1.toString()));
    }

    // Continue: for every test in test_public_all.py, translate into a @Test method here with equivalent logic.
    // For example: testFileExtensionDetectionPublic, testIsBinaryFilePublic, etc.

}