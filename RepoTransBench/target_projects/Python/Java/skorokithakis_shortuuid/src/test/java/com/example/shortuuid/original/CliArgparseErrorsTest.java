package com.example.shortuuid.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.example.shortuuid.Cli;

class CliArgparseErrorsTest {

    @Test
    void testCliInvalidArguments() {
        // Test unknown command
        String[] args1 = {"bogus"};
        Exception ex1 = assertThrows(IllegalArgumentException.class, () -> Cli.main(args1));
        assertTrue(ex1.getMessage().toLowerCase().contains("invalid") || ex1.getMessage().toLowerCase().contains("unknown"));

        // Fail 'encode' if no UUID
        String[] args2 = {"encode"};
        Exception ex2 = assertThrows(IllegalArgumentException.class, () -> Cli.main(args2));
        assertTrue(ex2.getMessage().toLowerCase().contains("usage") || ex2.getMessage().toLowerCase().contains("argument"));

        // Fail 'decode' if no shortuuid
        String[] args3 = {"decode"};
        Exception ex3 = assertThrows(IllegalArgumentException.class, () -> Cli.main(args3));
        assertTrue(ex3.getMessage().toLowerCase().contains("usage") || ex3.getMessage().toLowerCase().contains("argument"));
    }
}