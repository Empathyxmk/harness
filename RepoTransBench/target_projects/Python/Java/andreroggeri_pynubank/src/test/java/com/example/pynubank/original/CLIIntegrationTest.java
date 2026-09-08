package com.example.pynubank.original;

import com.example.pynubank.core.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.*;
import java.io.IOException;

public class CLIIntegrationTest {

    private static Path certPath() {
        return Paths.get(System.getProperty("user.dir"), "cert.p12");
    }

    private static void clean() {
        Path cert = certPath();
        if (Files.exists(cert)) {
            try {
                Files.delete(cert);
            } catch (IOException ignored) {}
        }
    }

    @Test
    void testShouldGenerateCerts() {
        clean();
        CLI simCLI = new CLI();
        simCLI.generateCertificate();
        assertTrue(Files.exists(certPath()));
        clean();
    }

    @Test
    void testRequestCodeExceptionShouldStopExecution() {
        clean();
        CLI simCLI = new CLI();
        try {
            simCLI.failGeneration();
        } catch (NuException e) {
            // Expected to fail.
        }
        assertFalse(Files.exists(certPath()));
        clean();
    }
}