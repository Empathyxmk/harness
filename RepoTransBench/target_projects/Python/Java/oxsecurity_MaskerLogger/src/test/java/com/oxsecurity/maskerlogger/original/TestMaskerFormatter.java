package com.oxsecurity.maskerlogger.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.regex.*;

import java.util.logging.*;

import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatter;
import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatterJson;
import com.oxsecurity.maskerlogger.maskerformatter.AbstractMaskedLogger;

public class TestMaskerFormatter {

    static class DummyRecord extends LogRecord {
        public DummyRecord(String msg) {
            super(Level.INFO, msg);
            setLoggerName("foo");
            setSourceClassName(TestMaskerFormatter.class.getName());
            setSourceMethodName("test");
        }
    }

    @Test
    public void testNoMaskingIfNoMatch() {
        MaskerFormatter formatter = new MaskerFormatter("%(message)s", null);
        DummyRecord rec = new DummyRecord("nothing secret here");
        String out = formatter.format(rec);
        assertEquals("nothing secret here", out);
    }

    @Test
    public void testMaskingWithRegexMatch() {
        MaskerFormatter formatter = new MaskerFormatter("%(message)s", null);
        DummyRecord rec = new DummyRecord("password: hunter2");
        String out = formatter.format(rec);
        assertTrue(out.contains("***"));
    }

    @Test
    public void testSkipMask() {
        MaskerFormatterJson formatter = new MaskerFormatterJson("%(message)s");
        DummyRecord rec = new DummyRecord("skip masking please");
        rec.setResourceBundleName("skip_mask"); // simulate apply_mask = false
        String out = formatter.format(rec);
        assertEquals("skip masking please", out);
    }

    @Nested
    class TestAbstractMaskedLogger {
        @Test
        public void testMaskSecret() {
            AbstractMaskedLogger logger = new AbstractMaskedLogger(null);
            Pattern p = Pattern.compile("(hunter2)");
            Matcher m = p.matcher("password: hunter2");
            assertTrue(m.find());
            String masked = logger._maskSecret("password: hunter2", new Matcher[]{m});
            assertTrue(masked.contains("***"));
        }
    }
}