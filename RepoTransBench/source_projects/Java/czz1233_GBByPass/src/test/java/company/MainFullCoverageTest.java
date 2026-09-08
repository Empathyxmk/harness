package company;

import org.junit.Test;
import java.io.*;

import static org.junit.Assert.*;

public class MainFullCoverageTest {

    @Test
    public void testMainWithNoArgs() throws Exception {
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        Main.main(new String[]{});
        System.setOut(originalOut);
        String output = baos.toString();
        // Only check that we get any output
        assertTrue(output.length() > 0);
    }

    @Test
    public void testMainWithNormalArg() throws Exception {
        String[] args = {"4567"};
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        Main.main(args);
        System.setOut(originalOut);
        String output = baos.toString();
        assertTrue(output.length() > 0);
    }

    @Test
    public void testMainWithAlphaArg() throws Exception {
        String[] args = {"abc123"};
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        Main.main(args);
        System.setOut(originalOut);
        String output = baos.toString();
        assertTrue(output.length() > 0);
    }

    @Test
    public void testMainWithEmptyArg() throws Exception {
        String[] args = {""};
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        Main.main(args);
        System.setOut(originalOut);
        String output = baos.toString();
        assertTrue(output.length() > 0);
    }
}