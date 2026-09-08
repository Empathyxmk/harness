package com.example.pynubank.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class PublicSetupPyFunctionalTest {

    @Test
    void testReadSuccess() throws IOException {
        Path tmpFile = Files.createTempFile("publicfile", null);
        Files.write(tmpFile, "PUBDATA".getBytes(StandardCharsets.UTF_8));
        String data = read(tmpFile.toString());
        assertEquals("PUBDATA", data);
        Files.delete(tmpFile);
    }

    @Test
    void testReadFileNotFound() {
        assertThrows(FileNotFoundException.class, () -> read("idonotexist_public.txt"));
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