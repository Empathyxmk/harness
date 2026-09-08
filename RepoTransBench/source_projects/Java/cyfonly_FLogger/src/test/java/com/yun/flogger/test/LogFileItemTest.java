package com.yun.flogger.test;

import com.cyfonly.flogger.strategy.LogFileItem;
import org.junit.Test;

import java.util.ArrayList;

import static org.junit.Assert.*;

public class LogFileItemTest {

    @Test
    public void testLogFileItemFields() {
        LogFileItem lfi = new LogFileItem();
        assertEquals("", lfi.logFileName);
        assertEquals("", lfi.fullLogFileName);
        assertEquals(0, lfi.currLogSize);
        assertEquals('A', lfi.currLogBuff);
        assertNotNull(lfi.alLogBufA);
        assertNotNull(lfi.alLogBufB);
        assertTrue(lfi.alLogBufA.isEmpty());
        assertTrue(lfi.alLogBufB.isEmpty());
        assertEquals(0, lfi.nextWriteTime);
        assertEquals("", lfi.lastPCDate);
        assertEquals(0, lfi.currCacheSize);

        lfi.alLogBufA.add(new StringBuffer("test A"));
        lfi.alLogBufB.add(new StringBuffer("test B"));
        assertEquals(1, lfi.alLogBufA.size());
        assertEquals(1, lfi.alLogBufB.size());
    }
}