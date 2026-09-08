package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MainSmokePublicTest {

    @Test
    void testMainLaunch() {
        // Pass some random args to make sure Main.main does not throw
        try {
            String[] args = {"hello", "world", "--flag"};
            Main.main(args);
        } catch(Exception e) {
            fail("Main.main() threw exception: " + e);
        }
    }
}