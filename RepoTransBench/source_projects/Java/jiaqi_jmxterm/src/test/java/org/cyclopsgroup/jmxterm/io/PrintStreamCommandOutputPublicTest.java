package org.cyclopsgroup.jmxterm.io;

import org.junit.Test;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.Assert.*;

public class PrintStreamCommandOutputPublicTest {

    @Test
    public void testOutputPrintsMessage() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream ps = new PrintStream(out);
        PrintStreamCommandOutput po = new PrintStreamCommandOutput(ps);
        String testMessage = "PublicTestLine 42";
        po.print(testMessage);
        po.flush();
        String result = out.toString();
        assertTrue("Expected output to contain our test message", result.contains(testMessage));
    }

    @Test
    public void testOutputPrintsAnotherMessage() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream ps = new PrintStream(out);
        PrintStreamCommandOutput po = new PrintStreamCommandOutput(ps);
        String testMessage = "AnotherUniquePublicTest";
        po.println(testMessage);
        po.flush();
        String result = out.toString();
        assertTrue("Output should contain unique printed value", result.contains(testMessage));
    }
}