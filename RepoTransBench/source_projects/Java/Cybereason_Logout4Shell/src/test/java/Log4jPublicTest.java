import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.ThreadContext;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.Assert.*;

public class Log4jPublicTest {
    private PrintStream originalOut;
    private PrintStream originalErr;
    private ByteArrayOutputStream outContent;
    private ByteArrayOutputStream errContent;

    @Before
    public void setUp() {
        originalOut = System.out;
        originalErr = System.err;
        outContent = new ByteArrayOutputStream();
        errContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        System.setErr(new PrintStream(errContent));
        ThreadContext.clearAll();
    }

    @After
    public void tearDown() {
        System.setOut(originalOut);
        System.setErr(originalErr);
        ThreadContext.clearAll();
    }

    @Test
    public void testConfigureLoggerWithThreadContext() {
        Log4j.configureLoggerWithThreadContext();
        Logger logger = LogManager.getLogger(Log4jPublicTest.class);
        ThreadContext.put("header", "PUBLIC_HEADER");
        logger.error("Another error!");
        String output = outContent.toString();
        assertTrue(output.contains("PUBLIC_HEADER"));
        assertTrue(output.contains("Another error!"));
    }

    @Test
    public void testMainWithThreadLocalAttack() {
        String[] args = {"-t"};
        Log4j.main(args);
        String output = outContent.toString();
        assertTrue(output.contains("Will use ThreadContext as attack vector"));
        assertTrue(output.contains("Vulnerable through thread context - 1"));
        assertTrue(output.contains("Vulnerable through thread context - 2"));
    }

    @Test
    public void testMainWithoutThreadLocalAttack() {
        String[] args = {};
        Log4j.main(args);
        String output = outContent.toString();
        // use a modified string to test for the presence of JNDI/LDAP pattern (don't use the exact string)
        assertTrue(output.contains("ldap://127.0.0.1:1389"));
        assertTrue(output.contains("${jndi:"));
    }
}