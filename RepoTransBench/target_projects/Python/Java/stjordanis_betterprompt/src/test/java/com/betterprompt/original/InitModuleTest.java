package com.betterprompt.original;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.lang.reflect.Field;

public class InitModuleTest {
    @Test
    public void testAllExports() throws Exception {
        for (String name : BetterPrompt.__all__) {
            boolean found = false;

            // Try as static field
            try {
                Field f = BetterPrompt.class.getField(name);
                found = true;
            } catch (NoSuchFieldException e) {
                // Try as method
                for (java.lang.reflect.Method m : BetterPrompt.class.getDeclaredMethods()) {
                    if (m.getName().equals(name)) {
                        found = true;
                        break;
                    }
                }
            }
            assertTrue(found, "Export '" + name + "' should be available in BetterPrompt.");
        }
    }
}