package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.scripts.ReadZBar;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestScriptsReadZbarPublic {
    @Test
    void testCreateArgParserAndHelp() {
        ReadZBar.ArgParser parser = ReadZBar.createArgParser();
        assertTrue(parser.hasOption("quiet"), "Parser must have 'quiet' option");
        assertTrue(parser.hasOption("file"), "Parser must have 'file' option");
    }

    @Test
    void testHelpOption() {
        ReadZBar.ArgParser parser = ReadZBar.createArgParser();
        String help = parser.getHelp();
        assertTrue(help.toLowerCase().contains("usage"));
    }
}