package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Setup {
    public static String python_requires = ">=2.7";
    public static void status(String x) {}
    public static void setup() {}
}

public class PublicTestSetup {

    @Test
    void testSetupImportsPublic() {
        assertNotNull(Setup.class.getDeclaredMethods());
        try {
            Setup.status("test");
            Setup.setup();
        } catch (Exception e) {
            fail();
        }
    }

    @Test
    void testPythonRequiresPublic() {
        assertTrue(Setup.python_requires.contains(">=2.7"));
    }
}