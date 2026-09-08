package com.example.localllm.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PublicModelDownloadTest {

    @Test
    public void testPublicDefaultFilename() {
        String repoId = "SomeAuthor/Mistral-Medium-AI-GGUF";
        String filename = ModelDownload.defaultFilename(repoId);
        assertTrue(filename.toLowerCase().endsWith(".gguf"));
        assertTrue(filename.toLowerCase().contains("mistral-medium"));
    }

    @Test
    public void testPublicDefaultFilenameLowercase() {
        String repoId = "anotherone/gpt-foo-gguf";
        String filename = ModelDownload.defaultFilename(repoId);
        assertTrue(filename.toLowerCase().endsWith(".gguf"));
        assertTrue(filename.toLowerCase().contains("gpt-foo"));
    }
}