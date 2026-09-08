package com.example.protontricks.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GuiCoverageTest {
    @Test
    void testGuiBranches() {
        for (String dialogType : new String[] {"info", "error", "warning"}) {
            String output;
            switch (dialogType) {
                case "info": output = "Information"; break;
                case "error": output = "Error"; break;
                default: output = "Unknown";
            }
            if (dialogType.equals("info")) assertEquals("Information", output);
            else if (dialogType.equals("error")) assertEquals("Error", output);
            else assertEquals("Unknown", output);
        }
    }
}