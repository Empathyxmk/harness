package com.baidu.pikaq.demo.service;

import org.junit.Test;
import static org.junit.Assert.*;

public class DBTest {
    @Test
    public void testDBNameConstant() {
        assertEquals("pikaqDemoWeb", DB.DB_NAME);
    }
}