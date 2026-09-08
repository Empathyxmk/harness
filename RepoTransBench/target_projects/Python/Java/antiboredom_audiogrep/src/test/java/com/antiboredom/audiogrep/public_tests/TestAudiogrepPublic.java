package com.antiboredom.audiogrep.public_tests;

import com.antiboredom.audiogrep.Audiogrep;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.nio.file.Path;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestAudiogrepPublic {
    @TempDir
    Path tmpPath;

    @Test
    public void testGetFilesPublic() throws Exception {
        Audiogrep ag = new Audiogrep();
        File a = tmpPath.resolve("file1.aac").toFile();
        File b = tmpPath.resolve("file2.m4a").toFile();
        File c = tmpPath.resolve("file3.txt").toFile();
        a.createNewFile();
        b.createNewFile();
        c.createNewFile();
        java.nio.file.Files.write(a.toPath(), "test abc".getBytes());
        java.nio.file.Files.write(b.toPath(), "test abc".getBytes());
        java.nio.file.Files.write(c.toPath(), "test abc".getBytes());

        Set<String> fs = new HashSet<>(ag.getFiles(tmpPath.toString(), List.of(".aac", ".m4a")));
        Set<String> expected = new HashSet<>(List.of(a.getAbsolutePath(), b.getAbsolutePath()));
        assertEquals(expected, fs);
    }
}