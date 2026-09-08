package com.example.utils;

import org.junit.Test;

public class LogUtilsTest {
    @Test
    public void testNoInstantiation() {
        boolean thrown = false;
        try {
            new LogUtils();
        } catch (Error e) {
            thrown = true;
        }
        assert thrown;
    }
}