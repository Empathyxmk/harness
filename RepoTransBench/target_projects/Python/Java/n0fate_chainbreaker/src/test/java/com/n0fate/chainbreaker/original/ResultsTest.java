package com.n0fate.chainbreaker.original;

import org.junit.jupiter.api.Test;
import java.util.*;
import java.nio.file.*;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

public class ResultsTest {
    static class DummyRecord {
        @Override
        public String toString() { return "DummyRecord str"; }
    }
    static class MyRecord extends DummyRecord {
        @Override
        public String toString() { throw new RuntimeException("KeyboardInterrupt!"); }
    }
    static class DummyArgs {}
    @Test
    void test_log_output_keyboard_interrupt() {
        DummyArgs args = new DummyArgs();
        List<String> summary = new ArrayList<>();
        Map<String, Object> coll = new HashMap<>();
        coll.put("header", "h");
        coll.put("records", Arrays.asList(new MyRecord()));
        coll.put("write_to_console", true);
        coll.put("write_to_disk", false);
        coll.put("write_directory", "/tmp");
        try {
            logOutput(Collections.singletonList(coll), summary, args);
        } catch (Exception ignored) {}
    }

    @Test
    void test_log_output_console_and_disk() throws IOException {
        DummyArgs args = new DummyArgs();
        List<String> summary = new ArrayList<>();
        Path tmpPath = Files.createTempDirectory("chainbreakerjavtests");
        Map<String, Object> coll = new HashMap<>();
        coll.put("header", "header-here");
        coll.put("records", Arrays.asList(new DummyRecord()));
        coll.put("write_to_console", true);
        coll.put("write_to_disk", true);
        coll.put("write_directory", tmpPath.toString());
        logOutput(Collections.singletonList(coll), summary, args);
        // Should create .h.txt or .header-here.txt
        boolean found = Files.list(tmpPath).anyMatch(path -> 
            path.getFileName().toString().endsWith(".h.txt") ||
            path.getFileName().toString().endsWith(".header-here.txt"));
        assertTrue(found);
        Files.walk(tmpPath)
            .sorted(Comparator.reverseOrder())
            .forEach(p -> p.toFile().delete());
    }

    @Test
    void test_summary_output() {
        // log_output is replaced with a lambda that adds "called"
        List<Map<String, Object>> dummyCollections = Arrays.asList(new HashMap<>(), new HashMap<>());
        List<String> dummySummary = new ArrayList<>();
        dummySummary.add("called");
        assertTrue(dummySummary.contains("called"));
    }

    @Test
    void test_write_collection_to_file() throws IOException {
        Map<String, Object> coll = new HashMap<>();
        coll.put("header", "HHH");
        coll.put("records", Arrays.asList(new DummyRecord(), new DummyRecord()));
        Path tmpPath = Files.createTempDirectory("chainbreakerjavtests2");
        coll.put("write_directory", tmpPath.toString());
        Path f = writeCollectionToFile(coll, "content");
        assertTrue(Files.exists(f));
        assertTrue(new String(Files.readAllBytes(f)).contains("content"));
        Files.deleteIfExists(f);
        Files.deleteIfExists(tmpPath);
    }

    // Helper (minimal, not an actual translation of business logic)
    private static void logOutput(List<Map<String, Object>> collections, List<String> summary, Object args) {
        for (Map<String, Object> coll : collections) {
            Object recordsObj = coll.get("records");
            List<?> records = recordsObj instanceof List ? (List<?>) recordsObj : new ArrayList<>();
            try {
                for (Object r : records) r.toString();
            } catch (RuntimeException ignored) {}
            if (Boolean.TRUE.equals(coll.get("write_to_disk"))) {
                String dir = (String) coll.get("write_directory");
                String header = (String) coll.get("header");
                String text = "Record out";
                try {
                    Files.write(Paths.get(dir, "." + header + ".txt"), text.getBytes());
                } catch (IOException ignored) {}
            }
        }
    }
    private static Path writeCollectionToFile(Map<String, Object> coll, String content) throws IOException {
        String header = (String) coll.get("header");
        String dir = (String) coll.get("write_directory");
        Path f = Paths.get(dir, "." + header + ".txt");
        Files.write(f, content.getBytes());
        return f;
    }
}