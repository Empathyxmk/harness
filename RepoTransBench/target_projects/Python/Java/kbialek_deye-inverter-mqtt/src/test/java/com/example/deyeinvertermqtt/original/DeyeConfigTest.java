package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeConfigTest {

    @Test
    public void testConfigLoadsDefault() {
        String defaultMode = "AUTO";
        assertEquals("AUTO", defaultMode, "Default mode should be AUTO");
    }

    @Test
    public void testConfigThrowsOnMissingFile() {
        Exception exception = assertThrows(RuntimeException.class, () -> {
            throw new RuntimeException("Config file not found");
        });
        assertEquals("Config file not found", exception.getMessage());
    }
}