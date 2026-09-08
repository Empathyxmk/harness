package top.niunaijun.blackobfuscator.core;

import org.junit.*;
import java.io.*;
import java.util.*;

import static org.junit.Assert.*;

public class MappingTest {
    private File mappingFile;

    @Before
    public void setUp() throws Exception {
        mappingFile = File.createTempFile("mapping", ".txt");
        try(PrintWriter pw = new PrintWriter(mappingFile)) {
            pw.println("# This is a comment");
            pw.println("com.abc.ClassA -> com.obf.X:");
            pw.println("  # Indented comment");
            pw.println("com.abc.ClassB -> com.obf.Y:");
            pw.println("bad mapping line");
            pw.println("com.abc.ClassC -> com.obf.Z:"); // extra for search coverage
        }
    }

    @Test
    public void testValidMappings() {
        Mapping mapping = new Mapping(mappingFile.getAbsolutePath());
        assertEquals("com.obf.X", mapping.get("com.abc.ClassA"));
        assertEquals("com.obf.Y", mapping.get("com.abc.ClassB"));
        assertEquals("com.obf.Z", mapping.get("com.abc.ClassC"));
        assertNull(mapping.get("com.abc.NotExist"));
        assertTrue(mapping.getMapping().size() >= 3);
    }

    @Test
    public void testNullFile() {
        Mapping m = new Mapping(null);
        assertNotNull(m.getMapping());
        assertTrue(m.getMapping().isEmpty());
    }

    @Test
    public void testNonExistentFile() {
        Mapping m = new Mapping("fakefile_doesnot_exist.txt");
        assertNotNull(m.getMapping());
        assertTrue(m.getMapping().isEmpty());
    }

    @Test
    public void testMalformedLines() throws Exception {
        File malformedFile = File.createTempFile("malformed", ".txt");
        try(PrintWriter pw = new PrintWriter(malformedFile)) {
            pw.println("malformed_line");
            pw.println("com.onlyonepart -> ");
            pw.println(" -> onlysecondpart:");
            pw.println("correct.package -> correct.target:");
        }
        Mapping m = new Mapping(malformedFile.getAbsolutePath());
        assertEquals("correct.target", m.get("correct.package"));
        malformedFile.delete();
    }

    @After
    public void tearDown() {
        mappingFile.delete();
    }
}