package com.baidu.pikaq.demo.service;

import org.junit.Test;
import static org.junit.Assert.*;

public class DBPublicTest {
    @Test
    public void testDBNameConstantDifferent() {
        // Checking same constant, but using contains for a different assertion style/coverage
        assertTrue(DB.DB_NAME.contains("DemoWeb"));
    }
}