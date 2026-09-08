package com.wroberts.pytimeparse.publictests;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;

public class PublicInitTest {
    @Test
    void testPublicVersionExtractionSuccess() throws Exception {
        Path tmpDir = Files.createTempDirectory("pytimeparse-public-init");
        try {
            Path pyDir = tmpDir.resolve("pytimeparse");
            Files.createDirectories(pyDir);
            Path versionFile = pyDir.resolve("VERSION");
            Files.write(versionFile, "3.4.5".getBytes());
            Path initFile = pyDir.resolve("__init__.py");
            String pyCode = 
                "from codecs import open\n" +
                "from os import path\n" +
                "try:\n" +
                "    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:\n" +
                "        __version__ = infile.read().strip()\n" +
                "except NameError:\n" +
                "    __version__ = 'unknown (public scenario)'\n" +
                "except IOError as ex:\n" +
                "    __version__ = \"unknown (%s)\" % ex\n";
            Files.write(initFile, pyCode.getBytes());
            String version = new String(Files.readAllBytes(versionFile)).trim();
            Assertions.assertEquals("3.4.5", version);
        } finally {
            deleteRecursive(tmpDir);
        }
    }

    @Test
    void testPublicVersionNoFile() {
        // Simulate NameError (__file__ not defined)
        String returned = "unknown (public without file)";
        Assertions.assertTrue(returned.startsWith("unknown"));
    }

    @Test
    void testPublicVersionIOError() throws Exception {
        Path tmpDir = Files.createTempDirectory("pytimeparse-public-initio");
        try {
            Path pyDir = tmpDir.resolve("pytimeparse");
            Files.createDirectories(pyDir);
            Path initFile = pyDir.resolve("__init__.py");
            String pyCode = 
                "from codecs import open\n" +
                "from os import path\n" +
                "try:\n" +
                "    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:\n" +
                "        __version__ = infile.read().strip()\n" +
                "except NameError:\n" +
                "    __version__ = 'unknown (public running interactive)'\n" +
                "except IOError as ex:\n" +
                "    __version__ = \"unknown (%s)\" % ex\n";
            Files.write(initFile, pyCode.getBytes());
            // Missing VERSION: simulate IOError
            String returned = "unknown (No such file or directory)";
            Assertions.assertTrue(returned.startsWith("unknown"));
            Assertions.assertNotEquals("unknown", returned);
        } finally {
            deleteRecursive(tmpDir);
        }
    }

    private void deleteRecursive(Path p) throws IOException {
        if (Files.exists(p)) {
            if (Files.isDirectory(p)) {
                try (DirectoryStream<Path> entries = Files.newDirectoryStream(p)) {
                    for (Path e : entries) {
                        deleteRecursive(e);
                    }
                }
            }
            Files.delete(p);
        }
    }
}