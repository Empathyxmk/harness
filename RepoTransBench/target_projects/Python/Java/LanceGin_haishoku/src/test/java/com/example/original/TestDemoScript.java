package com.example.original;

import org.junit.jupiter.api.Test;

import java.io.File;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

public class TestDemoScript {

    @Test
    public void testDemoFileExists() {
        File demoPy = Paths.get(System.getProperty("user.dir"), "demo", "demo.py").toFile();
        assertTrue(demoPy.exists());
    }

    @Test
    public void testDemoPngExists() {
        File demoPng = Paths.get(System.getProperty("user.dir"), "demo", "demo_01.png").toFile();
        assertTrue(demoPng.exists());
    }
}