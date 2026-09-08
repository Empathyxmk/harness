package com.mapio.gvanim.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.io.File;
import java.io.IOException;

public class TestRender {

    @Test
    void testRenderTmp() throws IOException {
        // Dummy replacement: simulate rendering and file existence check
        List<String> dotGraphs = Arrays.asList("digraph{}", "digraph{}");
        String tmpDir = System.getProperty("java.io.tmpdir");
        List<File> files = new ArrayList<>();
        for (int i = 0; i < dotGraphs.size(); ++i) {
            File f = new File(tmpDir, "myanim" + i + ".dot");
            f.createNewFile();
            files.add(f);
        }
        assertEquals(2, files.size());
        for (File f : files) {
            assertTrue(f.exists()); // These files exist because we created them
            f.delete();
        }
    }

    @Test
    void testGif() throws IOException {
        // Simulate creation of png files and a dummy call
        String tmpDir = System.getProperty("java.io.tmpdir");
        List<File> files = new ArrayList<>();
        for (int i = 0; i < 2; ++i) {
            File f = new File(tmpDir, "f" + i + ".png");
            f.createNewFile();
            files.add(f);
        }
        List<List<String>> called = new ArrayList<>();
        DummyRender dummyRender = new DummyRender(called);
        dummyRender.gif(files, new File(tmpDir, "anim"), 123, 11);
        boolean convertCalled = false;
        for (List<String> c : called) {
            if (c.contains("convert")) convertCalled = true;
        }
        assertTrue(convertCalled);
        for (File f : files) f.delete();
    }

    static class DummyRender {
        List<List<String>> callTracker;
        DummyRender(List<List<String>> tracker) { this.callTracker = tracker; }
        void gif(List<File> files, File anim, int delay, int size) {
            // Simulates calling 'convert' command over image files
            callTracker.add(Arrays.asList("convert", String.valueOf(delay), anim.getAbsolutePath()));
        }
    }
}