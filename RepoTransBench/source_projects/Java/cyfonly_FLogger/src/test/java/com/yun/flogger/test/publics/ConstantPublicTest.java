package com.yun.flogger.test.publics;

import com.cyfonly.flogger.constants.Constant;
import org.junit.Test;
import static org.junit.Assert.*;

public class ConstantPublicTest {

    @Test
    public void testLevelsAndMapPublic() {
        // Use FATAL (4) instead of INFO as in originals etc
        assertEquals(4, Constant.FATAL);
        assertEquals("FATAL", Constant.LOG_DESC_MAP.get("4"));
        assertEquals("DEBUG", Constant.LOG_DESC_MAP.get("0"));
        assertNotNull(Constant.CFG_LOG_LEVEL);
        assertTrue(Constant.CFG_LOG_LEVEL.contains("4"));
    }

    @Test
    public void testCharsetAndPathPublic() {
        assertNotNull(Constant.CFG_CHARSET_NAME);
        assertNotNull(Constant.CFG_LOG_PATH);
        assertTrue(Constant.CFG_CHARSET_NAME.toUpperCase().contains("UTF"));
        assertTrue(Constant.CFG_LOG_PATH.contains("log"));
    }
}