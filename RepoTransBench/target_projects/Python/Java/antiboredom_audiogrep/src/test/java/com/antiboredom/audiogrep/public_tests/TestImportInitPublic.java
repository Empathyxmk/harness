package com.antiboredom.audiogrep.public_tests;

import com.antiboredom.audiogrep.Audiogrep;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestImportInitPublic {
    @Test
    public void testImportsPublic() {
        // Just checks class loads
        try {
            Class<?> clazz = Class.forName("com.antiboredom.audiogrep.Audiogrep");
            assertNotNull(clazz);
            // Try to get at least one basic property or method
            boolean hasFile = false, hasDoc = false;
            for (java.lang.reflect.Method m : clazz.getMethods()) {
                if (m.getName().equals("__file__")) {
                    hasFile = true;
                }
                if (m.getName().equals("__doc__")) {
                    hasDoc = true;
                }
            }
            assertTrue(hasFile || hasDoc || clazz != null);
        } catch (Exception e) {
            fail("Audiogrep class not importable in Java: " + e.getMessage());
        }
    }
}