package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

class PublicRedirectTest {
    @Test
    void testRedirectOutputToFile() throws IOException {
        File f = File.createTempFile("redirect_test", ".txt");
        f.deleteOnExit();
        try (FileWriter writer = new FileWriter(f)) {
            writer.write("hello world\n");
        }
        String content;
        try (BufferedReader reader = new BufferedReader(new FileReader(f))) {
            content = reader.readLine();
        }
        assertEquals("hello world", content);
    }

    @Test
    void testRedirectAppendToFile() throws IOException {
        File f = File.createTempFile("redirect_test_append", ".txt");
        f.deleteOnExit();
        try (FileWriter writer = new FileWriter(f)) {
            writer.write("a\n");
        }
        try (FileWriter writer = new FileWriter(f, true)) {
            writer.write("b\n");
        }
        List<String> readLines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(f))) {
            String ln;
            while ((ln = reader.readLine()) != null) {
                readLines.add(ln);
            }
        }
        assertIterableEquals(Arrays.asList("a", "b"), readLines);
    }
}