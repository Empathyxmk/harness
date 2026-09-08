package com.example.utils;

import org.junit.Test;

public class AnimationUtilsTest {
    @Test
    public void testNoInstantiation() {
        boolean thrown = false;
        try {
            new AnimationUtils();
        } catch (Error e) {
            thrown = true;
        }
        assert thrown;
    }
}