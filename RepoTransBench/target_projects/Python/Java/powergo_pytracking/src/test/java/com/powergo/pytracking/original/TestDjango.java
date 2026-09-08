package com.powergo.pytracking.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestDjango {

    @Test
    void testSimpleDjangoSettings() {
        class DjangoSettings {
            String env = "prod";
        }
        DjangoSettings settings = new DjangoSettings();
        assertEquals("prod", settings.env);
    }
}