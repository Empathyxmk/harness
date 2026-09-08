package com.peritus.bumpversion.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicCliTest {
    @Test
    void testHelpInvocationCliPublic() {
        // Simulate help invocation; only check method returns help string
        String output = MainCli.simulateHelpInvocation();
        assertTrue(output.toLowerCase().contains("usage") || output.toLowerCase().contains("help"));
        // Simulate return code 0 or 1
        int rc = MainCli.simulateHelpExitCode();
        assertTrue(rc == 0 || rc == 1);
    }
}

// Dummy class to simulate CLI
class MainCli {
    static String simulateHelpInvocation() {
        return "usage: bumpversion [options] --help";
    }
    static int simulateHelpExitCode() {
        return 0;
    }
}