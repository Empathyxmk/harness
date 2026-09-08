package com.hannesdorfmann.fragmentargs;

import org.junit.Test;

public class FragmentArgsInjectorTest {

    @Test
    public void injectorInterfaceShouldAllowAnyObject() {
        FragmentArgsInjector inj = new FragmentArgsInjector() {
            @Override
            public void inject(Object target) {
                // no-op
            }
        };
        inj.inject("dummy");
    }
}