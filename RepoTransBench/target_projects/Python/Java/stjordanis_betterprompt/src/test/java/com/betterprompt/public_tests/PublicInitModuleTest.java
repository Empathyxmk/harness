package com.betterprompt.public_tests;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicInitModuleTest {
    @Test
    public void testPublicAllExports() {
        for (String name : BetterPrompt.__all__) {
            boolean found = false;
            try {
                BetterPrompt.class.getField(name);
                found = true;
            } catch (NoSuchFieldException e) {
                for (java.lang.reflect.Method m : BetterPrompt.class.getDeclaredMethods()) {
                    if (m.getName().equals(name)) {
                        found = true;
                        break;
                    }
                }
            }
            assertTrue(found, "Export (by name) should exist as field or method: " + name);
        }
    }
}