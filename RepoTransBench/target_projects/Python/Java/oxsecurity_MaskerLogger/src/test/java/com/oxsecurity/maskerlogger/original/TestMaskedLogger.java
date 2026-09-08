package com.oxsecurity.maskerlogger.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.regex.*;
import java.io.File;
import java.nio.file.Paths;
import java.util.logging.*;

import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatter;
import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatterJson;
import com.oxsecurity.maskerlogger.maskerformatter.AbstractMaskedLogger;

public class TestMaskedLogger {

    private static final String TEST_CONFIG_PATH = 
        Paths.get(new File(System.getProperty("user.dir")).getParent(), 
                  "maskerlogger", "config", "gitleaks.toml").toString();

    static class DummyRecord extends LogRecord {
        public DummyRecord(String msg) {
            super(Level.WARNING, msg);
            setLoggerName("foo");
            setSourceClassName(TestMaskedLogger.class.getName());
            setSourceMethodName("test");
        }
    }

    private MaskerFormatter formatter;
    private MaskerFormatterJson jsonFormatter;
    private String fmt;

    @BeforeEach
    public void setUp() {
        fmt = "%(levelname)s %(message)s";
        formatter = new MaskerFormatter(fmt, TEST_CONFIG_PATH, 75);
        jsonFormatter = new MaskerFormatterJson("%(message)s", TEST_CONFIG_PATH, 50);
    }

    @Test
    public void testMaskSecretLogic() {
        AbstractMaskedLogger logger = new AbstractMaskedLogger(TEST_CONFIG_PATH);
        Pattern p = Pattern.compile("(a)(b+)");
        Matcher match = p.matcher("abbbbb");
        assertTrue(match.find());
        String msg = logger._maskSecret("abbbbb start abbbbb", new Matcher[]{match});
        assertTrue(msg.chars().filter(c -> c == '*').count() > 0);
    }

    @Test
    public void testMaskSensitiveDataNoMatch() {
        AbstractMaskedLogger logger = new AbstractMaskedLogger(TEST_CONFIG_PATH);
        DummyRecord record = new DummyRecord("no secrets here");
        logger._maskSensitiveData(record);
        assertEquals("no secrets here", record.getMessage());
    }

    @Test
    public void testMaskSensitiveDataWithMatch() {
        AbstractMaskedLogger logger = new AbstractMaskedLogger(TEST_CONFIG_PATH);
        DummyRecord record = new DummyRecord("\"password\": \"password321\" and apikey = 1234");
        logger.setRedact(45);
        logger._maskSensitiveData(record);
        assertTrue(record.getMessage() instanceof String);
        assertFalse(record.getMessage().contains("password321"));
    }

    @Test
    public void testFormatterFullLogIntegration() {
        Logger logger = Logger.getLogger("logtest");
        logger.setLevel(Level.INFO);
        Handler handler = new StreamHandler(System.out, formatter);
        logger.addHandler(handler);
        try {
            logger.info("\"current_key\": \"AIzaSOHbouG6DDa6DOcRGEgOMayAXYXcw6la3c\"");
            logger.info("\"AKIAI44QH8DHBEXAMPLE\" and then more text.");
            logger.info("Datadog access token: 'abcdef1234567890abcdef1234567890'");
            logger.info("\"password\": \"password123\"");
        } finally {
            logger.removeHandler(handler);
        }
    }

    @Test
    public void testJsonFormatterLogrecordMasking() {
        DummyRecord rec = new DummyRecord("apikey = \"TESTEXPOSEDSECRET\"");
        String value = jsonFormatter.format(rec);
        assertTrue(value.contains("apikey"));
    }

    @Test
    public void testMaskerFormatterJsonSkipMask() {
        DummyRecord rec = new DummyRecord("sometext");
        rec.setResourceBundleName("skip_mask"); // simulate apply_mask = false
        // Should not attempt masking
        String result = jsonFormatter.format(rec);
        assertTrue(result.contains("sometext"));
    }

    @Test
    public void testReprAndStr() {
        String name = jsonFormatter.getClass().getSimpleName();
        assertTrue(name.contains("Json"));
    }
}