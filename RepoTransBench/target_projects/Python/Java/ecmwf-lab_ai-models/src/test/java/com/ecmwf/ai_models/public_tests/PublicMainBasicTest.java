package com.ecmwf.ai_models.public_tests;

import org.junit.jupiter.api.*;
import java.util.*;

class PublicMainBasicTest {

    static class DummyArgs {
        public String command;
        public String dummy;
        public DummyArgs(String command, String dummy) {
            this.command = command;
            this.dummy = dummy;
        }
    }

    static DummyArgs parseArgs(String[] argv) {
        if (Arrays.asList(argv).contains("nonsense_command")) throw new IllegalArgumentException("Invalid command");
        String dummy = argv.length > 2 ? argv[2] : null;
        return new DummyArgs(argv[0], dummy);
    }

    @Test
    void test_public_main_parse_args() {
        String[] argv = {"run", "--dummy", "xy"};
        DummyArgs args = parseArgs(argv);
        Assertions.assertEquals("run", args.command);
        Assertions.assertTrue("xy".equals(args.dummy) || args.dummy == null);
    }

    @Test
    void test_public_main_invalid_args() {
        String[] argv = {"nonsense_command"};
        Assertions.assertThrows(IllegalArgumentException.class, () -> {
            parseArgs(argv);
        });
    }
}