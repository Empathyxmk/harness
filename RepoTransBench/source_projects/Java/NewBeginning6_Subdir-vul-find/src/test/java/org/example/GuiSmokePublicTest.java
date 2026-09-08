package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class GuiSmokePublicTest {

    @Test
    void testBasicGuiInstantiation() {
        // Just check if Gui can be constructed (smoke test)
        try {
            Gui gui = new Gui();
            assertNotNull(gui);
        } catch(Exception e) {
            fail("Gui instantiation failed: " + e);
        }
    }
}