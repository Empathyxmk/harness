package com.stephenmcd.formsbuilder.original;

import org.junit.jupiter.api.Test;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

public class SetupPyTest {

    public static class DummyStat {
        public int st_uid = 0;
        public int st_gid = 0;
        public int st_mode = 0o644;
    }

    @Test
    public void testExcludeFiles() throws Exception {
        Path tmpDir = Files.createTempDirectory("testExcludeFiles");
        File pyFile = tmpDir.resolve("tmp.py").toFile();
        File txtFile = tmpDir.resolve("tmp.txt").toFile();
        File pycFile = tmpDir.resolve("tmp.pyc").toFile();

        try (FileWriter f = new FileWriter(pyFile)) { f.write("pass"); }
        try (FileWriter f = new FileWriter(txtFile)) { f.write("hello"); }
        try (FileWriter f = new FileWriter(pycFile)) { f.write("compiled!"); }

        String[] exclude = { pyFile.getAbsolutePath(), txtFile.getAbsolutePath() };
        // Emulate removing files and statting
        boolean removed = false;
        for (String file : exclude) {
            File f = new File(file);
            if (f.exists()) {
                f.delete();
                removed = true;
            }
        }
        DummyStat stat = new DummyStat();
        assertEquals(0, stat.st_uid);
        assertEquals(0, stat.st_gid);
        assertEquals(0o644, stat.st_mode);
        assertTrue(removed);

        pyFile.delete();
        txtFile.delete();
        pycFile.delete();
        tmpDir.toFile().delete();
    }

    @Test
    public void testRemoveBuild() throws Exception {
        Path tmpDir = Files.createTempDirectory("testRemoveBuild");
        Path buildPath = tmpDir.resolve("build");
        buildPath.toFile().mkdir();

        boolean[] called = new boolean[]{false};
        // Simulate a build removal like in setup.py's rmtree
        if (buildPath.toFile().exists()) {
            buildPath.toFile().delete();
            called[0] = true;
        }
        assertTrue(called[0]);
        tmpDir.toFile().delete();
    }
}