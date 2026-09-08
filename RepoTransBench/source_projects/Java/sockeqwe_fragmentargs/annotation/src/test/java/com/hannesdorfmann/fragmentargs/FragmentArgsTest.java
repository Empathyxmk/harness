package com.hannesdorfmann.fragmentargs;

import org.junit.Test;
import static org.junit.Assert.*;

public class FragmentArgsTest {

    static class DummyInjector implements FragmentArgsInjector {
        boolean injected = false;

        @Override
        public void inject(Object target) {
            injected = true;
        }
    }

    @Test
    public void testInjectWithNoAutoMappingClass() {
        // Should not throw even if injector cannot be found.
        FragmentArgs.inject(new Object());
    }

    @Test
    public void testInjectWithAutoMappingInjectorPresent() throws Exception {
        // Set up a custom classloader that will "inject" our DummyInjector and reset static field for test isolation.
        // Reflection hack to inject our DummyInjector instance.
        DummyInjector dummy = new DummyInjector();
        java.lang.reflect.Field field = FragmentArgs.class.getDeclaredField("autoMappingInjector");
        field.setAccessible(true);
        field.set(null, dummy);

        Object fragment = new Object();
        FragmentArgs.inject(fragment);
        assertTrue(dummy.injected);

        // Clean up for other tests
        field.set(null, null);
    }
}