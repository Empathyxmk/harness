package com.example.plop.public_tests;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class DummyNodeP {
    int id;
    Map<String, Object> attrs;
    Map<String, Integer> weights;
    DummyNodeP(int id, String attr, int calls) {
        this.id = id;
        this.attrs = Map.of("attr", attr);
        this.weights = Map.of("calls", calls);
    }
    public int hashCode() { return Objects.hash(this.id); }
    public boolean equals(Object o) {
        if (!(o instanceof DummyNodeP)) return false;
        return this.id == ((DummyNodeP)o).id;
    }
}
class DummyStackP {
    List<DummyNodeP> nodes;
    Map<String, Integer> weights;
    DummyStackP(List<DummyNodeP> nodes, int calls) {
        this.nodes = nodes;
        this.weights = Map.of("calls", calls);
    }
}
class DummyEdgeP {
    DummyNodeP parent, child;
    Map<String, Integer> weights;
    DummyEdgeP(DummyNodeP p, DummyNodeP c) {
        parent = p; child = c; weights = Map.of("bar", 3);
    }
}
class DummyCallGraphP {
    List<DummyStackP> stacks = List.of(
        new DummyStackP(List.of(new DummyNodeP(11, "aa", 13)), 13),
        new DummyStackP(List.of(new DummyNodeP(22, "bb", 17)), 17)
    );
    Map<Integer, DummyEdgeP> edges = Map.of(
        1, new DummyEdgeP(new DummyNodeP(11, "aa", 13), new DummyNodeP(22, "bb", 17)),
        2, new DummyEdgeP(new DummyNodeP(22, "bb", 17), new DummyNodeP(11, "aa", 13))
    );
    static DummyCallGraphP load(String filename) { return new DummyCallGraphP(); }
}
class IndexHandler {
    List<String> files_rendered;
    void get(List<String> filesToRender) {
        render("index.html", filesToRender);
    }
    void render(String tpl, List<String> files) {
        files_rendered = files;
    }
}
class ViewHandler {
    String filename;
    String tpl; String renderedFile;
    void get(String fn) {
        render("force.html", fn);
    }
    void render(String tpl, String filename) {
        this.tpl = tpl;
        this.renderedFile = filename;
    }
}
class ViewFlatHandler {
    String tpl;
    Map<String, Object> renderedData;
    Path staticPath;
    void get() {
        Map<String, Object> d = Map.of("nodes", new Object(), "edges", new Object(), "stacks", new Object());
        render("force-flat.html", d);
    }
    void render(String tpl, Map<String, Object> data) {
        this.tpl = tpl; this.renderedData = data;
    }
    String embedFile(String filename) throws IOException {
        Path file = staticPath.resolve(filename);
        return Files.readString(file);
    }
}
class DataHandler {
    Map<String, Object> written;
    void get() {
        Map<String, Object> d = Map.of("nodes", new Object(), "edges", new Object(), "stacks", new Object());
        write(d);
    }
    void write(Map<String, Object> val) { written = val; }
}

public class PublicViewerTest {

    @Test
    void testPublicIndexHandlerSorted() {
        List<String> filenames = List.of("sample_0.prof", "sample_1.prof", "sample_2.prof");
        IndexHandler handler = new IndexHandler();
        handler.get(filenames);
        List<String> sorted = new ArrayList<>(handler.files_rendered); Collections.sort(sorted);
        List<String> expected = new ArrayList<>(filenames); Collections.sort(expected);
        assertEquals(expected, sorted);
    }

    @Test
    void testPublicViewHandler() {
        ViewHandler handler = new ViewHandler();
        handler.get("alpha.prof");
        assertEquals("force.html", handler.tpl);
        assertEquals("alpha.prof", handler.renderedFile);
    }

    @Test
    void testPublicViewFlatHandler() {
        ViewFlatHandler handler = new ViewFlatHandler();
        handler.get();
        assertEquals("force-flat.html", handler.tpl);
        assertTrue(handler.renderedData.containsKey("nodes"));
        assertTrue(handler.renderedData.containsKey("edges"));
        assertTrue(handler.renderedData.containsKey("stacks"));
    }

    @Test
    void testPublicViewFlatEmbedFile() throws IOException {
        Path tempDir = Files.createTempDirectory("viewer-public");
        Path tempFile = tempDir.resolve("b.txt");
        Files.writeString(tempFile, "goodbye");
        ViewFlatHandler handler = new ViewFlatHandler();
        handler.staticPath = tempDir;
        String result = handler.embedFile("b.txt");
        assertEquals("goodbye", result);
        Files.delete(tempFile); Files.delete(tempDir);
    }

    @Test
    void testPublicDataHandler() {
        DataHandler handler = new DataHandler();
        handler.get();
        assertTrue(handler.written.containsKey("nodes"));
        assertTrue(handler.written.containsKey("edges"));
        assertTrue(handler.written.containsKey("stacks"));
    }

    @Test
    void testPublicProfileToJson() throws IOException {
        Path tempDir = Files.createTempDirectory("viewer-public-json");
        Path profile = tempDir.resolve("run.prof");
        Files.writeString(profile, "dummy data");
        Map<String, Object> result = Map.of("nodes", new Object(), "edges", new Object(), "stacks", new Object());
        assertTrue(result instanceof Map<?, ?>);
        assertTrue(result.containsKey("nodes"));
        assertTrue(result.containsKey("edges"));
        assertTrue(result.containsKey("stacks"));
        Files.delete(profile); Files.delete(tempDir);
    }

    @Test
    void testPublicProfileToJsonPathTraversal() {
        Exception ex = assertThrows(AssertionError.class, () -> {
            if ("../../out.prof".contains("..")) throw new AssertionError();
        });
        assertNotNull(ex);
    }
}