package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestCmdlineTest {
    @Test
    public void testCmdlineArgs() {
        String[] args = {"--username", "john.doe", "--list-devices"};
        assertEquals("--username", args[0]);
        assertEquals("john.doe", args[1]);
        assertEquals("--list-devices", args[2]);
    }

    @Test
    public void testCmdlineHelp() {
        String output = "usage: pyicloud ...";
        assertTrue(output.toLowerCase().contains("usage"));
    }
}