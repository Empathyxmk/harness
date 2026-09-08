package com.example.pynubank.public;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.*;
import java.io.IOException;

public class PublicCliTest {

    private static Path certPath() {
        return Paths.get(System.getProperty("user.dir"), "public_cert.p12");
    }

    private static void clean() {
        Path path = certPath();
        if (Files.exists(path)) {
            try {
                Files.delete(path);
            } catch (IOException ignored) {}
        }
    }

    @Test
    void testShouldGenerateCerts() {
        clean();
        CLI cli = new CLI();
        cli.generateCertificate();
        assertTrue(Files.exists(certPath()));
        clean();
    }
}