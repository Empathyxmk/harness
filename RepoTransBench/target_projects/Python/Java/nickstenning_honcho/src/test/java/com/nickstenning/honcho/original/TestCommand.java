package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Command;

class TestCommand {

    @Test
    void testBuildCommandList() {
        Command command = new Command("echo", "Hello", "World");
        String[] commandList = command.getCommandList();
        assertArrayEquals(new String[]{"echo", "Hello", "World"}, commandList);
    }

    @Test
    void testCommandToString() {
        Command command = new Command("ls", "-l", "/tmp");
        assertEquals("ls -l /tmp", command.toString());
    }
}