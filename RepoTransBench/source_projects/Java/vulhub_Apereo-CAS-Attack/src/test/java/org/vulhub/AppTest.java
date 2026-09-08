package org.vulhub;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

class AppTest {

    @Test
    void testMainNoArgs() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(out));
        App.main(new String[]{});
        System.setOut(old);
        assertTrue(out.toString().contains("Hello from Apereo CAS Attack tool!"));
    }

    @Test
    void testMainAttackCasTarget() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(out));
        App.main(new String[]{"attack", "cas-server"});
        System.setOut(old);
        assertTrue(out.toString().contains("Simulating CAS attack on cas-server"));
    }

    @Test
    void testMainAttackNonCasTarget() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(out));
        App.main(new String[]{"attack", "notcas"});
        System.setOut(old);
        // The logic in App.java only returns "Target is not a CAS server: <target>" 
        // if target does NOT contain "cas" (lowercase) substring
        // "notcas" contains "cas", so it matches the "cas" check and thus is considered a CAS server
        // So the output will contain "Simulating CAS attack on notcas"
        assertTrue(out.toString().contains("Simulating CAS attack on notcas"));
    }

    @Test
    void testMainAttackNoTarget() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(out));
        App.main(new String[]{"attack"});
        System.setOut(old);
        assertTrue(out.toString().contains("No target specified for attack."));
    }

    @Test
    void testMainHelp() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(out));
        App.main(new String[]{"help"});
        System.setOut(old);
        assertTrue(out.toString().contains("Usage: java -jar apereo-cas-attack.jar"));
    }

    @Test
    void testMainUnknownCommand() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream old = System.out;
        System.setOut(new PrintStream(out));
        App.main(new String[]{"unknown"});
        System.setOut(old);
        String output = out.toString();
        assertTrue(output.contains("Unknown command: unknown"));
        assertTrue(output.contains("Usage: java -jar apereo-cas-attack.jar"));
    }

    @Test
    void testPerformAttackNull() {
        assertEquals("No target specified for attack.", App.performAttack(null));
    }

    @Test
    void testPerformAttackCasTarget() {
        assertEquals("Simulating CAS attack on cas-server", App.performAttack("cas-server"));
    }

    @Test
    void testPerformAttackNonCasTarget() {
        // Since "something" does not contain "cas", it is not detected as a CAS target.
        assertEquals("Target is not a CAS server: something", App.performAttack("something"));
    }

    @Test
    void testPerformAttackCasSubstringCaseInsensitive() {
        // The method checks for lowercase "cas". So "cAS" will not match.
        assertEquals("Target is not a CAS server: bestcASattack", App.performAttack("bestcASattack"));
    }
}