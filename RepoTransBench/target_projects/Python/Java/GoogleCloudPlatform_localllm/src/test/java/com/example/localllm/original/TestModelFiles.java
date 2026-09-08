package com.example.localllm.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.Arrays;

public class TestModelFiles {

    private final String[] files = new String[]{
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/.no_exist/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/tokenizer.model",
        "/home/user/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf",
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/config.json",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/refs/main",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf"
    };

    @Test
    public void testFilterModels() {
        var m = ModelFiles.filterModels(Arrays.asList(files));
        assertEquals(2, m.size());
        assertEquals("TheBloke/openinstruct-mistral-7B-GGUF", m.get(0)[0]);
        assertEquals("openinstruct-mistral-7b.Q4_K_M.gguf", m.get(0)[1]);
        assertEquals("TheBloke/smartyplats-7B-v2-GGUF", m.get(1)[0]);
        assertEquals("smartyplats-7b-v2.Q4_K_M.gguf", m.get(1)[1]);
    }

    @Test
    public void testModelFromPath() {
        String[] repoAndModel = ModelFiles.modelFromPath(
            "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf");
        assertEquals("TheBloke/Llama-2-13B-Ensemble-v5-GGUF", repoAndModel[0]);
        assertEquals("llama-2-13b-ensemble-v5.Q4_K_M.gguf", repoAndModel[1]);
    }

    @Test
    public void testModelFromPathUnknownFormat() {
        String[] repoAndModel = ModelFiles.modelFromPath("foo");
        assertEquals("", repoAndModel[0]);
        assertEquals("", repoAndModel[1]);
    }

    @Test
    public void testPathFromRepo() {
        String repoId = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF";
        String path = ModelFiles.pathFromRepo(repoId);
        assertTrue(path.endsWith(".cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF"));
    }

    @Test
    public void testPathFromRepoUnknownFormat() {
        String path = ModelFiles.pathFromRepo("SomeRepo");
        assertEquals("", path);
    }

    @Test
    public void testFindModel() {
        String model = "smartyplats-7b-v2.Q4_K_M.gguf";
        String path = ModelFiles.findModel(Arrays.asList(files), model);
        assertEquals(
            "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf", path);
    }
}