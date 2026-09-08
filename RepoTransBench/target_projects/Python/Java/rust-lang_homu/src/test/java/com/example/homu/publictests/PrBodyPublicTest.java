package com.example.homu.publictests;

import com.example.homu.main.Main;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PrBodyPublicTest {

    @Test
    public void testPrBodyContainsDiffKey() {
        String body = "Closes #99\nExtra: refactor code";
        assertTrue(Main.prBodyContains(body, "refactor"));
    }

    @Test
    public void testPrBodyNotContainsDiffKey() {
        String body = "Implements feature X.\nNone found.";
        assertFalse(Main.prBodyContains(body, "security"));
    }
}