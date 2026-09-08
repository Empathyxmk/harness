package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AppsMod {
    static class UuslugConfig {
        String name;
        String verbose_name;
        UuslugConfig(String name, String label) {
            this.name = name;
            this.verbose_name = "Uuslug app";
        }
    }
}

public class PublicTestAppsPy {
    @Test
    void testAppsConfigNamePublic() {
        AppsMod.UuslugConfig appConfig = new AppsMod.UuslugConfig("uuslug", "uuslug");
        assertEquals("uuslug", appConfig.name);
        assertNotNull(appConfig.verbose_name);
        assertTrue(appConfig.verbose_name.toLowerCase().contains("uuslug"));
    }
}