package com.hannesdorfmann.fragmentargs;

import org.junit.Test;
import static org.junit.Assert.*;

public class FragmentArgsPublicTest {

    static class AlternateDummyInjector implements FragmentArgsInjector {
        boolean invoked = false;

        @Override
        public void inject(Object target) {
            // Use different logic/data to differentiate
            if (target != null) {
                invoked = true;
            }
        }
    }

    @Test
    public void testInjectWithNoAutoMappingClass_differentInput() {
        // Inject a custom String (different input type/instance)
        FragmentArgs.inject("publicDummyString");
        // No assertions necessary (should not throw)
    }

    @Test
    public void testInjectWithAutoMappingInjectorPresent_differentInjector() throws Exception {
        AlternateDummyInjector altInjector = new AlternateDummyInjector();
        java.lang.reflect.Field field = FragmentArgs.class.getDeclaredField("autoMappingInjector");
        field.setAccessible(true);
        field.set(null, altInjector);

        Integer testTarget = 2024; // Different data type and value
        FragmentArgs.inject(testTarget);
        assertTrue(altInjector.invoked);

        // Clean up for other tests
        field.set(null, null);
    }
}