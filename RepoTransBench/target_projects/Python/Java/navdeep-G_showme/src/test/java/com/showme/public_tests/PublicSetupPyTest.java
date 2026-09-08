package com.showme.public_tests;

import com.showme.core.Core;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class PublicSetupPyTest {
    @Test
    void testPublicSetupMainRuns() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            Core.setupPyMain(new String[] {"--version"});
            String captured = out.toString();
            assertTrue(captured.contains("setup_py_main"));
        } finally {
            System.setOut(oldOut);
        }
    }
}