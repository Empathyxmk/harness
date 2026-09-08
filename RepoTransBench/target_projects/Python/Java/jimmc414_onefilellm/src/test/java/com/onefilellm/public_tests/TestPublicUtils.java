package com.onefilellm.public_tests;

import com.onefilellm.utils.Utils;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

class TestPublicUtils {

    @Test
    void testSafeFileReadUtf8AndFallbackPublic() throws IOException {
        Path tempFile = Files.createTempFile("foo", ".txt");
        String data = "Testing äßü";
        Files.writeString(tempFile, data, StandardCharsets.UTF_8);
        assertEquals(data, Utils.safeFileRead(tempFile.toString()));
        Files.delete(tempFile);

        Path tempFileLatin = Files.createTempFile("bar", ".txt");
        String latin = "niño";
        Files.write(tempFileLatin, latin.getBytes("ISO-8859-1"));
        assertEquals(latin, Utils.safeFileRead(tempFileLatin.toString()));
        Files.delete(tempFileLatin);
    }

    // Continue: for every test in test_public_utils.py, translate into a @Test method here with the equivalent logic.
    // Use parameterized tests as in the public version for table-driven patterns.
}