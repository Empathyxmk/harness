package com.example.localllm.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.util.*;

public class TestModelFilesFull {

    private static Path tmpPath;

    @BeforeAll
    public static void globalSetup() throws IOException {
        tmpPath = Files.createTempDirectory("test_hubcache");
    }

    private File createFakeModelDir(String repo, String model) throws IOException {
        String[] parts = repo.split("/");
        File repoDir = tmpPath.resolve("hubcache").resolve(String.format("models--%s--%s", parts[0], parts[1])).toFile();
        repoDir.mkdirs();
        File modelPath = new File(repoDir, model);
        Files.writeString(modelPath.toPath(), "fake model");
        return modelPath;
    }

    @Test
    public void testGetModelDirPatched() {
        // Patch modelfiles.getModelDir to return our tmp
        ModelFiles.setGetModelDirSupplier(() -> tmpPath.resolve("hubcache").toString());
        assertTrue(ModelFiles.getModelDir().contains(tmpPath.resolve("hubcache").toString()));
    }

    @Test
    public void testListModels() throws IOException {
        ModelFiles.setGetModelDirSupplier(() -> tmpPath.resolve("notfound").toString());
        assertEquals(0, ModelFiles.listModels().size());

        File modelFile = createFakeModelDir("foo/bar", "bar.Q4_K_M.gguf");
        ModelFiles.setGetModelDirSupplier(() -> tmpPath.resolve("hubcache").toString());
        List<File> files = ModelFiles.getAllFiles(modelFile.getParentFile().getParent());
        List<String[]> filtered = ModelFiles.filterModels(files);
        assertTrue(filtered.size() >= 1);
        assertEquals(filtered, ModelFiles.listModels());
    }

    @Test
    public void testFilterModelsAndModelFromPath() {
        List<File> files = Arrays.asList(
            new File("/some/fake/path/models--foo--bar/baz.Q4_K_M.gguf"),
            new File("/some/other/path/notamodel.txt")
        );
        List<String[]> filtered = ModelFiles.filterModels(files);
        assertTrue(filtered instanceof List);
        for (String[] tup : filtered) {
            assertTrue(tup instanceof String[] && tup.length == 2);
        }
    }

    @Test
    public void testModelFromPathVariants() {
        String path = "something/models--foo--bar/baz.Q4_K_M.gguf";
        String[] repoAndModel = ModelFiles.modelFromPath(path);
        assertEquals("foo/bar", repoAndModel[0]);
        assertEquals("baz.Q4_K_M.gguf", repoAndModel[1]);
        assertArrayEquals(new String[]{"", ""}, ModelFiles.modelFromPath("no-model-here"));
    }

    @Test
    public void testPathFromRepo() {
        ModelFiles.setGetModelDirSupplier(() -> tmpPath.resolve("hubcache").toString());
        String rv = ModelFiles.pathFromRepo("foo/bar");
        assertTrue(rv.contains("models--foo--bar"));

        assertEquals("", ModelFiles.pathFromRepo("foo"));
    }

    @Test
    public void testGetAllFiles() throws IOException {
        File fn = createFakeModelDir("foo/bar", "bar.Q4_K_M.gguf");
        List<File> out = ModelFiles.getAllFiles(fn.getParentFile().getParent());
        assertTrue(out.stream().anyMatch(f -> f.getName().endsWith(".gguf")));

        File empty = tmpPath.resolve("empty").toFile();
        empty.mkdir();
        assertEquals(0, ModelFiles.getAllFiles(empty.toString()).size());
    }

    @Test
    public void testPathFromModel() throws IOException {
        File fn = createFakeModelDir("foo/bar", "bar.Q4_K_M.gguf");
        String repoId = "foo/bar";
        String model = fn.getName();
        ModelFiles.setGetModelDirSupplier(() -> tmpPath.resolve("hubcache").toString());
        String out = ModelFiles.pathFromModel(repoId, model);
        assertNotNull(out);
        assertTrue(out.endsWith(model));
        assertNull(ModelFiles.pathFromModel("foo/bar", "notfound.model"));
    }

    @Test
    public void testFindModel() {
        List<String> files = Arrays.asList(
            "/root/test/1.Q4_K_M.gguf",
            "/root/test/2.Q4_K_M.gguf"
        );
        String found = ModelFiles.findModel(files, "1.Q4_K_M.gguf");
        assertTrue(found.endsWith("1.Q4_K_M.gguf"));
        assertNull(ModelFiles.findModel(files, "X.Q4_K_M.gguf"));
    }
}