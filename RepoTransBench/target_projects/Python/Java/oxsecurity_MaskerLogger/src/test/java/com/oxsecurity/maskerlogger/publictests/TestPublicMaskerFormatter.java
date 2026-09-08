package com.oxsecurity.maskerlogger.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.regex.*;

import java.util.logging.*;

import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatter;
import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatterJson;
import com.oxsecurity.maskerlogger.maskerformatter.AbstractMaskedLogger;

public class TestPublicMaskerFormatter {

    static class DummyRecord extends LogRecord {
        public DummyRecord(String msg) {
            super(Level.WARNING, msg);
            setLoggerName("dummy");
            setSourceClassName("some.Class");
            setSourceMethodName("test");
        }
    }

    @Test
    public void testNoMaskingIfNoMatchPublic() {
        MaskerFormatter formatter = new MaskerFormatter("%(message)s", null);
        DummyRecord rec = new DummyRecord("12345 is a safe message");
        String out = formatter.format(rec);
        assertEquals("12345 is a safe message", out);
    }

    @Test
    public void testMaskingWithRegexMatchPublic() {
        MaskerFormatter formatter = new MaskerFormatter("%(message)s", null);
        DummyRecord rec = new DummyRecord("apikey: mytopsecret");
        String out = formatter.format(rec);
        assertTrue(out.contains("***"));
    }

    @Test
    public void testSkipMaskPublic() {
        MaskerFormatterJson formatter = new MaskerFormatterJson("%(message)s");
        DummyRecord rec = new DummyRecord("nothing to mask here");
        rec.setResourceBundleName("skip_mask"); // simulate apply_mask = false
        String out = formatter.format(rec);
        assertEquals("nothing to mask here", out);
    }

    @Nested
    class TestAbstractMaskedLoggerPublic {
        @Test
        public void testMaskSecretPublic() {
            AbstractMaskedLogger logger = new AbstractMaskedLogger(null);
            Pattern p = Pattern.compile("(mytopsecret)");
            Matcher m = p.matcher("apikey: mytopsecret");
            assertTrue(m.find());
            String masked = logger._maskSecret("apikey: mytopsecret", new Matcher[]{m});
            assertTrue(masked.contains("***"));
        }
    }
}