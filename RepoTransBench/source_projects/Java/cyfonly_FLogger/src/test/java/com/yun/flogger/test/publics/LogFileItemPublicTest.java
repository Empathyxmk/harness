package com.yun.flogger.test.publics;

import com.cyfonly.flogger.strategy.LogFileItem;
import org.junit.Test;

import java.util.ArrayList;

import static org.junit.Assert.*;

public class LogFileItemPublicTest {

    @Test
    public void testLogFileItemFieldsWithDifferentData() {
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

        // Add different test values
        lfi.alLogBufA.add(new StringBuffer("public test AAA"));
        lfi.alLogBufB.add(new StringBuffer("public test BBB"));
        lfi.alLogBufA.add(new StringBuffer("extra item in A"));
        assertEquals(2, lfi.alLogBufA.size());
        assertEquals(1, lfi.alLogBufB.size());
        assertEquals("public test AAA", lfi.alLogBufA.get(0).toString());
        assertEquals("public test BBB", lfi.alLogBufB.get(0).toString());
        assertEquals("extra item in A", lfi.alLogBufA.get(1).toString());
    }
}