package com.showme.original;

import com.showme.core.Core;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class SetupPyTest {
    @Test
    void testPublishBranchSetupPyMain() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            Core.setupPyMain(new String[]{"publish"});
            String output = out.toString();
            assertTrue(output.contains("setup_py_main"));
        } finally {
            System.setOut(oldOut);
        }
    }

    @Test
    void testSetupRunsSetupPyMain() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            Core.setupPyMain(new String[]{"install"});
            String output = out.toString();
            assertTrue(output.contains("setup_py_main"));
        } finally {
            System.setOut(oldOut);
        }
    }
}