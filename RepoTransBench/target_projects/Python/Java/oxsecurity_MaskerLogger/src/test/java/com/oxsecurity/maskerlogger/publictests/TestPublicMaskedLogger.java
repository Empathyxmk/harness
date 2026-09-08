package com.oxsecurity.maskerlogger.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.regex.*;
import java.nio.file.Paths;
import java.io.File;
import java.util.logging.*;

import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatter;
import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatterJson;
import com.oxsecurity.maskerlogger.maskerformatter.AbstractMaskedLogger;

public class TestPublicMaskedLogger {

    private static final String TEST_CONFIG_PATH =
            Paths.get(new File(System.getProperty("user.dir")).getParent(),
                    "maskerlogger", "config", "gitleaks.toml").toString();

    static class DummyRecord extends LogRecord {
        public DummyRecord(String msg) {
            super(Level.SEVERE, msg);
            setLoggerName("dummy");
            setSourceClassName("public");
            setSourceMethodName("test");
        }
    }

    private MaskerFormatter formatter;
    private MaskerFormatterJson jsonFormatter;

    @BeforeEach
    public void setUp() {
        formatter = new MaskerFormatter("%(levelname)s: %(message)s", TEST_CONFIG_PATH, 33);
        jsonFormatter = new MaskerFormatterJson("%(message)s", TEST_CONFIG_PATH, 22);
    }

    @Test
    public void testMaskSecretLogicWithNewPattern() {
        AbstractMaskedLogger logger = new AbstractMaskedLogger(TEST_CONFIG_PATH);
        Pattern p = Pattern.compile("(x)(y+)");
        Matcher match = p.matcher("xyyyy");
        assertTrue(match.find());
        String msg = logger._maskSecret("xyyyy abc xyyyy", new Matcher[]{match});
        assertTrue(msg.chars().filter(c -> c == '*').count() > 0);
    }

    @Test
    public void testMaskSensitiveDataNoMatchNewmsg() {
        AbstractMaskedLogger logger = new AbstractMaskedLogger(TEST_CONFIG_PATH);
        DummyRecord record = new DummyRecord("totally safe entry");
        logger._maskSensitiveData(record);
        assertEquals("totally safe entry", record.getMessage());
    }

    @Test
    public void testMaskSensitiveDataWithMatchNewsecret() {
        AbstractMaskedLogger logger = new AbstractMaskedLogger(TEST_CONFIG_PATH);
        DummyRecord record = new DummyRecord("\"token\": \"abcd12345efgh\" and secret_key = zyxw");
        logger.setRedact(39);
        logger._maskSensitiveData(record);
        assertTrue(record.getMessage() instanceof String);
        assertFalse(record.getMessage().contains("abcd12345efgh"));
    }

    @Test
    public void testFormatterFullLogIntegrationPublic() {
        Logger logger = Logger.getLogger("logtest_public");
        logger.setLevel(Level.SEVERE);
        Handler handler = new StreamHandler(System.out, formatter);
        logger.addHandler(handler);
        try {
            logger.severe("\"another_key\": \"AIzaSoMEoth3rKEY344sdlGh289Ka3dLPd\"");
            logger.severe("\"AWS_SECRET_THISISFAKE\" and some more.");
            logger.severe("Datadog token is: 'zyxw9876zyxw9876zyxw9876zyxw9876'");
            logger.severe("\"pin\": \"5678\"");
        } finally {
            logger.removeHandler(handler);
        }
    }

    @Test
    public void testJsonFormatterLogrecordMaskingPublic() {
        DummyRecord rec = new DummyRecord("auth = \"FAKENEWSECRETXYZ\"");
        String value = jsonFormatter.format(rec);
        assertTrue(value.contains("auth"));
    }

    @Test
    public void testMaskerFormatterJsonSkipMaskPublic() {
        DummyRecord rec = new DummyRecord("publiclogtext");
        rec.setResourceBundleName("skip_mask"); // simulate apply_mask = false
        String result = jsonFormatter.format(rec);
        assertTrue(result.contains("publiclogtext"));
    }

    @Test
    public void testReprAndStrPublic() {
        String name = jsonFormatter.getClass().getSimpleName();
        assertTrue(name.contains("Json"));
    }
}