package org.usadellab.trimmomatic;

import org.junit.jupiter.api.*;
import java.io.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class DummyPublicFastqRecord extends org.usadellab.trimmomatic.fastq.FastqRecord {
    public DummyPublicFastqRecord(String n) {
        super(n, "TGCA", "@@@@");
    }
}

public class PairomaticPublicTest {

    private File createTempFastq(List<String> names, Character delimiter) throws IOException {
        File temp = File.createTempFile("pairo_pub", ".fastq");
        temp.deleteOnExit();
        PrintWriter w = new PrintWriter(temp);
        for (String n : names) {
            w.println("@" + n + (delimiter == null ? "" : delimiter+"2"));
            w.println("TGCA");
            w.println("+");
            w.println("@@@@");
        }
        w.close();
        return temp;
    }

    @Test
    void testGetFastqNamesDelimiterDash() throws IOException {
        Pairomatic p = new Pairomatic();
        List<String> names = Arrays.asList("QX", "ZE");
        File f = createTempFastq(names, '-');
        Set<String> result = invokeGetFastqNames(p, f, '-');
        assertEquals(2, result.size());
    }

    @Test
    void testGetFastqNamesNoDelimiterMultiple() throws IOException {
        Pairomatic p = new Pairomatic();
        List<String> names = Arrays.asList("A010", "B020");
        File f = createTempFastq(names, null);
        Set<String> result = invokeGetFastqNames(p, f, null);
        assertEquals(2, result.size());
    }

    @Test
    void testGetFastqNamesFailOnDelimiter() throws IOException {
        Pairomatic p = new Pairomatic();
        List<String> names = Arrays.asList("NM");
        File f = createTempFastq(names, null);
        Exception ex = assertThrows(RuntimeException.class, () -> {
            invokeGetFastqNames(p, f, '-');
        });
        assertTrue(ex.getMessage().contains("Failed to find expected delimiter"));
    }

    @Test
    void testEqualOrderingMismatch() {
        Pairomatic p = new Pairomatic();
        Set<String> s1 = new LinkedHashSet<>(Arrays.asList("U","V"));
        Set<String> s2 = new LinkedHashSet<>(Arrays.asList("V","U"));
        assertFalse(invokeEqualOrdering(p, s1, s2));
        Set<String> s3 = new LinkedHashSet<>(Arrays.asList("U","V"));
        assertTrue(invokeEqualOrdering(p, s1, s3));
    }

    // Reflection for private methods
    @SuppressWarnings("unchecked")
    private Set<String> invokeGetFastqNames(Pairomatic p, File f, Character d) {
        try {
            java.lang.reflect.Method m = Pairomatic.class.getDeclaredMethod("getFastqNames", File.class, Character.class);
            m.setAccessible(true);
            return (Set<String>)m.invoke(p, f, d);
        } catch(Exception e) { throw new RuntimeException(e); }
    }

    private boolean invokeEqualOrdering(Pairomatic p, Set<String> s1, Set<String> s2) {
        try {
            java.lang.reflect.Method m = Pairomatic.class.getDeclaredMethod("equalOrdering", Set.class, Set.class);
            m.setAccessible(true);
            return (boolean)m.invoke(p, s1, s2);
        } catch(Exception e) { throw new RuntimeException(e); }
    }
}