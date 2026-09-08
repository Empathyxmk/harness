package com.example.localllm.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PublicModelFilesTest {

    @Test
    public void testPublicModelFromPathShortformat() {
        String[] result = ModelFiles.modelFromPath("/mnt/bob/models/elephant/banana.Q4_1.gguf");
        assertEquals("elephant", result[0]);
        assertEquals("banana.Q4_1.gguf", result[1]);
    }

    @Test
    public void testPublicModelFromPathLonger() {
        String[] result = ModelFiles.modelFromPath("/home/user/some/other/hippo/hippopotamus.Q5_0.gguf");
        assertEquals("hippo", result[0]);
        assertEquals("hippopotamus.Q5_0.gguf", result[1]);
    }
}