package com.example.original;

import static org.junit.jupiter.api.Assertions.*;

import com.example.sample.Init;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class TestInit {

    private final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
    private final PrintStream originalOut = System.out;

    @BeforeEach
    public void setUpStreams() {
        System.setOut(new PrintStream(outContent));
    }

    @Test
    void testMainPrintsMessage() {
        Init.main(new String[]{});
        String output = outContent.toString().trim();
        assertTrue(output.contains("Call your main application code here"),
            "Output should contain the expected message.");
    }
}