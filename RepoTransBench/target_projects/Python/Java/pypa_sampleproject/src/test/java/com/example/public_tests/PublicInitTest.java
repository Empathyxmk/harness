package com.example.public_tests;

import static org.junit.jupiter.api.Assertions.*;

import com.example.sample.Init;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

class PublicInitTest {

    private final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
    private final PrintStream originalOut = System.out;

    @BeforeEach
    void setUpStreams() {
        System.setOut(new PrintStream(outContent));
    }

    @Test
    void testMainPrintsCustomMessage() {
        Init.main(new String[]{});
        String output = outContent.toString();
        assertTrue(output.contains("main application code"),
            "Output should contain 'main application code'.");
    }
}