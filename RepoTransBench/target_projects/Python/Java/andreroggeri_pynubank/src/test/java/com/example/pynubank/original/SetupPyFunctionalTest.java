package com.example.pynubank.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class SetupPyFunctionalTest {

    @Test
    void testReadSuccess() throws IOException {
        Path tmpFile = Files.createTempFile("afile", null);
        Files.write(tmpFile, "DATA".getBytes(StandardCharsets.UTF_8));
        String data = read(tmpFile.toString());
        assertEquals("DATA", data);
        Files.delete(tmpFile);
    }

    @Test
    void testReadFileNotFound() {
        assertThrows(FileNotFoundException.class, () -> read("idonotexist.txt"));
    }

    private String read(String fname) throws IOException {
        try (BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(fname), StandardCharsets.UTF_8))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) sb.append(line);
            return sb.toString();
        }
    }
}