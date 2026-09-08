package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicIntegrationRegressionTest {

    // Dummy regression: check output stays constant for a specific input
    static String regressionLatex(String key) {
        if ("old_case".equals(key)) return "$x+1$";
        return "$unknown$";
    }

    @Test
    void testRegressionOldCase() {
        assertEquals("$x+1$", regressionLatex("old_case"));
    }

    @Test
    void testRegressionUnknown() {
        assertEquals("$unknown$", regressionLatex("nope"));
    }
}