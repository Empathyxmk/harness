package com.example.localllm.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class TestModelDownload {

    @Test
    public void testDefaultFilename() {
        String repoId = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF";
        String filename = ModelDownload.defaultFilename(repoId);
        assertEquals("llama-2-13b-ensemble-v5.Q4_K_M.gguf", filename);
    }

    @Test
    public void testDefaultFilenameUnknownFormat() {
        String filename = ModelDownload.defaultFilename("foo");
        assertEquals("", filename);
    }

    @Test
    public void testDefaultFilenameUnsupportedExt() {
        String repoId = "TheBloke/openinstruct-mistral-7B-GPTQ";
        String filename = ModelDownload.defaultFilename(repoId);
        assertEquals("", filename);
    }
}