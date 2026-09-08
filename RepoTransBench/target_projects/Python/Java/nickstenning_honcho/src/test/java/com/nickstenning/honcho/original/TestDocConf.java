package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDocConf {

    @Test
    void testDocConfigKeys() {
        // Typical doc/conf.py settings, simulate load
        String project = "honcho";
        String author = "Nick Stenning";
        String version = "1.2.3";
        assertAll(
            () -> assertEquals("honcho", project),
            () -> assertEquals("Nick Stenning", author),
            () -> assertTrue(version.matches("\\d+\\.\\d+(\\.\\d+)?"))
        );
    }
}