package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestAppsPy {

    // Simulate AppConfig for Django
    static class UuslugConfig {
        private final String name = "uuslug";
        private final String verboseName = "UUSLUG";

        public String getName() { return name; }
        public String getVerboseName() { return verboseName; }
    }

    @Test
    void testAppConfigNameAndVerboseName() {
        UuslugConfig config = new UuslugConfig();
        assertEquals("uuslug", config.getName());
        assertEquals("UUSLUG", config.getVerboseName());
    }
}