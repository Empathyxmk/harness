package com.example.shortuuid.original;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

import com.example.shortuuid.ShortUUID;
import com.example.shortuuid.Main;
import com.example.shortuuid.Cli;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class CliTest {

    private final PrintStream originalOut = System.out;
    private ByteArrayOutputStream outContent;

    @BeforeEach
    void setUp() {
        outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent, true, StandardCharsets.UTF_8));
    }

    @AfterEach
    void tearDown() {
        System.setOut(originalOut);
    }

    @Test
    void testCliEncodeAndDecode() {
        // Test encode
        String uuidStr = UUID.randomUUID().toString();
        String[] argsEncode = {"encode", uuidStr};
        Cli.main(argsEncode);
        String outEncode = outContent.toString().trim();
        assertNotNull(outEncode);
        assertTrue(outEncode.length() > 0);

        // Prepare for decode
        outContent.reset();
        String[] argsDecode = {"decode", outEncode};
        Cli.main(argsDecode);
        String outDecode = outContent.toString().trim();
        // Should be a UUID, so verify parse succeeds
        UUID parsed = UUID.fromString(outDecode);
        assertNotNull(parsed);
    }

    @Test
    void testCliDecodeLegacy() {
        UUID u = UUID.randomUUID();
        String shortStr = Main.encode(u);
        String reversed = new StringBuilder(shortStr).reverse().toString();
        outContent.reset();
        String[] args = {"decode", reversed, "--legacy"};
        Cli.main(args);
        String out = outContent.toString().trim();
        UUID parsed = UUID.fromString(out);
        assertNotNull(parsed);
    }

    @Test
    void testCliNoFn() {
        // No subcommand: just invoke Main.uuid() and print result
        outContent.reset();
        String[] args = {};
        Cli.main(args);
        String out = outContent.toString().trim();
        assertNotNull(out);
        assertTrue(out instanceof String);
        assertTrue(out.length() > 0);
    }
}