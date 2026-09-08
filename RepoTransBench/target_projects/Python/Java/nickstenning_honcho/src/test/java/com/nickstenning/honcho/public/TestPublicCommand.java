package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Command;

class TestPublicCommand {
    @Test
    void testPublicCommandList() {
        Command command = new Command("pwd");
        String[] commandList = command.getCommandList();
        assertArrayEquals(new String[]{"pwd"}, commandList);
    }
}