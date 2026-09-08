package com.hannesdorfmann.fragmentargs;

import org.junit.Test;

public class FragmentArgsInjectorPublicTest {

    @Test
    public void injectorInterfaceShouldAllowAnyObject_publicTest() {
        FragmentArgsInjector inj = new FragmentArgsInjector() {
            @Override
            public void inject(Object target) {
                // still accepts any target, use different type
                if (target instanceof Double) {
                    // no-op
                }
            }
        };
        inj.inject(77.7); // pass a Double, different from original test
    }
}