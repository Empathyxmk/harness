package com.yun.flogger.test;

import com.cyfonly.flogger.constants.Constant;
import org.junit.Test;
import static org.junit.Assert.*;

public class ConstantTest {

    @Test
    public void testLogLevels() {
        assertEquals(0, Constant.DEBUG);
        assertEquals(1, Constant.INFO);
        assertEquals(2, Constant.WARN);
        assertEquals(3, Constant.ERROR);
        assertEquals(4, Constant.FATAL);
    }

    @Test
    public void testLogDescMap() {
        assertEquals("DEBUG", Constant.LOG_DESC_MAP.get("0"));
        assertEquals("INFO", Constant.LOG_DESC_MAP.get("1"));
        assertEquals("WARN", Constant.LOG_DESC_MAP.get("2"));
        assertEquals("ERROR", Constant.LOG_DESC_MAP.get("3"));
        assertEquals("FATAL", Constant.LOG_DESC_MAP.get("4"));
    }

    @Test
    public void testConfigDefaults() {
        assertNotNull(Constant.CFG_LOG_LEVEL);
        assertTrue(Constant.CFG_CHARSET_NAME.equalsIgnoreCase("UTF-8"));
        assertTrue(Constant.CFG_LOG_PATH != null);
    }
}