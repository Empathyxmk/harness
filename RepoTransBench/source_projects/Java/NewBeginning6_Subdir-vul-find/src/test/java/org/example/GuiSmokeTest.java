package org.example;

import org.junit.jupiter.api.Test;

public class GuiSmokeTest {
    @Test
    void testMain() {
        // Smoke test for coverage, won't actually render a window in CI
        String[] args = { "--help" };
        Gui.main(args);
    }
}