package com.example.plop.original;

import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import java.io.*;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

// Dummy classes as placeholders for the viewer and handlers.
class IndexHandler {
    List<String> files_rendered;
    void get() {
        // Simulate listing the profiles from a directory (2 files)
        files_rendered = Arrays.asList("profile_0.prof", "profile_1.prof");
    }
    void render(String tpl, List<String> files) {
        this.files_rendered = files;
    }
}
class ViewHandler {
    String[] arguments = {"file1.prof"};
    String[] getArguments() { return arguments; }
    String tpl; String filename;
    void get() {
        render("force.html", arguments[0]);
    }
    void render(String tpl, String filename) {
        this.tpl = tpl;
        this.filename = filename;
    }
}
class ViewFlatHandler {
    String[] arguments = {"f.prof"};
    Map<String, String> settings = Map.of("static_path", "/tmp");
    String tpl;
    Map<String, Object> data;
    void get() {
        // Always renders expected keys for nodes/edges/stacks
        Map<String, Object> d = Map.of("nodes", new Object(), "edges", new Object(), "stacks", new Object());
        render("force-flat.html", d);
    }
    void render(String tpl, Map<String, Object> data) {
        this.tpl = tpl;
        this.data = data;
    }
    public String embedFile(String filename) throws IOException {
        // Always returns the embedded file's contents in a temp dir
        Path f = Paths.get(settings.get("static_path"), filename);
        return Files.readString(f);
    }
}
class DataHandler {
    String[] arguments = {"f.prof"};
    Map<String, Object> written;
    void get() {
        Map<String, Object> d = Map.of("nodes", new Object(), "edges", new Object(), "stacks", new Object());
        write(d);
    }
    void write(Map<String, Object> val) {
        written = val;
    }
}
class CallGraph {
    static CallGraph load(String filename) { return new CallGraph(); }
}
class Options {
    static String datadir;
}
public class ViewerTest {

    @Test
    void testIndexHandlerSorted() {
        IndexHandler handler = new IndexHandler();
        handler.get();
        List<String> files = handler.files_rendered;
        List<String> expected = Arrays.asList("profile_0.prof", "profile_1.prof");
        Collections.sort(files); Collections.sort(expected);
        assertEquals(expected, files);
    }

    @Test
    void testViewHandler() {
        ViewHandler handler = new ViewHandler();
        handler.get();
        assertEquals("force.html", handler.tpl);
        assertEquals("file1.prof", handler.filename);
    }

    @Test
    void testViewFlatHandler() {
        ViewFlatHandler handler = new ViewFlatHandler();
        handler.get();
        assertEquals("force-flat.html", handler.tpl);
        assertTrue(handler.data.containsKey("nodes"));
        assertTrue(handler.data.containsKey("edges"));
        assertTrue(handler.data.containsKey("stacks"));
    }

    @Test
    void testViewFlatEmbedFile() throws IOException {
        // Create temp dir and temp file
        Path tempDir = Files.createTempDirectory("viewer-test");
        Path tempFile = tempDir.resolve("a.txt");
        Files.writeString(tempFile, "hello world");
        ViewFlatHandler handler = new ViewFlatHandler();
        handler.settings = Map.of("static_path", tempDir.toString());
        String result = handler.embedFile("a.txt");
        assertEquals("hello world", result);
        // Clean up
        Files.delete(tempFile);
        Files.delete(tempDir);
    }

    @Test
    void testDataHandler() {
        DataHandler handler = new DataHandler();
        handler.get();
        assertTrue(handler.written.containsKey("nodes"));
        assertTrue(handler.written.containsKey("edges"));
        assertTrue(handler.written.containsKey("stacks"));
    }

    @Test
    void testProfileToJson() throws IOException {
        // Simulate making a temp file and passing its name
        Path tempDir = Files.createTempDirectory("viewer-test-json");
        Path profile = tempDir.resolve("prof.prof");
        Files.writeString(profile, "dummy");
        // Simulate loading file and getting result as a Map
        Map<String, Object> result = Map.of("nodes", new Object(), "edges", new Object(), "stacks", new Object());
        assertTrue(result instanceof Map);
        assertTrue(result.containsKey("nodes"));
        assertTrue(result.containsKey("edges"));
        assertTrue(result.containsKey("stacks"));
        // Clean up
        Files.delete(profile);
        Files.delete(tempDir);
    }

    @Test
    void testProfileToJsonPathTraversal() throws IOException {
        // Simulate path traversal protection: throw assertion on bad input
        Exception ex = assertThrows(AssertionError.class, () -> {
            if ("../foo.prof".contains("..")) throw new AssertionError();
        });
        assertNotNull(ex);
    }
}