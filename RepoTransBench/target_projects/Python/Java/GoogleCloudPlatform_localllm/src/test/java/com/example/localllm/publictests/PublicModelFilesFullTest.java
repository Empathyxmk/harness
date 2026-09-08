package com.example.localllm.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.Arrays;
import java.util.List;

public class PublicModelFilesFullTest {

    @Test
    public void testPublicFindLlmFiles() {
        String testDir = "/tmp/some-llm-model-dir";
        String[] testFiles = new String[] {"lion.Q4_0.gguf", "giraffe.Q8_0.gguf"};
        Mockito.mockStatic(java.io.File.class)
            .when(() -> new java.io.File(testDir).list()).thenReturn(testFiles);

        Mockito.mockStatic(java.io.File.class)
            .when(() -> new java.io.File(testDir).isDirectory()).thenReturn(true);

        List<String> output = ModelFiles.findLlmfiles(testDir);
        boolean foundGguf = false;
        for (String f : output) foundGguf |= f.endsWith(".gguf");
        assertTrue(foundGguf, "Should find at least one .gguf file");
        assertTrue(output.toString().contains("lion.Q4_0.gguf"));
    }

    @Test
    public void testPublicIsLlmfile() {
        assertTrue(ModelFiles.isLlmfile("rhino.Q7_0.gguf"));
        assertFalse(ModelFiles.isLlmfile("zebra.txt"));
    }
}