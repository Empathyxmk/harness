package com.example.utils;

import org.junit.Test;

public class PicassoUtilTest {
    @Test
    public void testNoInstantiation() {
        boolean thrown = false;
        try {
            new PicassoUtil();
        } catch (Error e) {
            thrown = true;
        }
        assert thrown;
    }
}