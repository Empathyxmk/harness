package com.example.public_tests;

import org.junit.jupiter.api.Test;
import java.io.File;

import static org.junit.jupiter.api.Assertions.*;

public class PublicDemoScriptTest {

    @Test
    public void testDemoPngExists() {
        File demoPng = new File("demo/demo_01.png");
        assertTrue(demoPng.exists());
    }
}