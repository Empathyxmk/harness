package com.example.localllm.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mockito;
import org.mockito.stubbing.Answer;

import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class TestModelDownloadFull {

    private ModelDownload modeldownload;
    private ModelFiles modelfiles;

    @BeforeEach
    public void setUp() {
        // Assuming ModelDownload and ModelFiles are Java classes provided in src/main...
        modeldownload = Mockito.mock(ModelDownload.class, Mockito.CALLS_REAL_METHODS);
        modelfiles = Mockito.mock(ModelFiles.class, Mockito.CALLS_REAL_METHODS);
    }

    @Test
    public void testDefaultFilenameValid() {
        Mockito.when(modelfiles.getDEFAULT_FILE_EXT()).thenReturn("gguf");
        String repoId = "TheBloke/foo-123-gguf";
        // Simulate static method by class delegation or static mocking
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.getDEFAULT_FILE_EXT()).thenReturn("gguf");
        String result = ModelDownload.defaultFilename(repoId);
        assertEquals("foo-123.Q4_K_M.gguf", result);
    }

    @Test
    public void testDefaultFilenameInvalid() {
        String badRepo = "broken";
        assertEquals("", ModelDownload.defaultFilename(badRepo));

        String repoBad = "foo/bar-model";
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.getDEFAULT_FILE_EXT()).thenReturn("ggufx");
        assertEquals("", ModelDownload.defaultFilename(repoBad));

        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.getDEFAULT_FILE_EXT()).thenReturn("gguf");
        assertEquals("", ModelDownload.defaultFilename("foo/bar-model-xyz"));
    }

    @Test
    public void testDownloadCallsHfHubDownload() {
        // To mock static method: require external tool or a wrapper, so let's assume a wrapper
        HfHubDownloadWrapper hfHubDownload = Mockito.mock(HfHubDownloadWrapper.class); // replace with actual
        Mockito.when(hfHubDownload.hfHubDownload("foo", "bar")).thenReturn("downloaded_path");
        String result = ModelDownload.download("foo", "bar", hfHubDownload);
        assertEquals("downloaded_path", result);
        Mockito.verify(hfHubDownload).hfHubDownload("foo", "bar");
    }

    @Test
    public void testRemoveFile() {
        String repoId = "foo/bar";
        String filename = "model.gguf";
        String blobPath = "/somewhere/model.gguf";

        // Patch functions
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.pathFromModel(repoId, filename)).thenReturn(blobPath);
        Mockito.mockStatic(java.nio.file.Files.class).when(() -> java.nio.file.Files.exists(Paths.get(blobPath))).thenReturn(true);

        List<String> rmCalled = new ArrayList<>();
        ModelDownload.setRemoveCallback(s -> rmCalled.add(s)); // hypothetical hook for testing

        ModelDownload.remove(repoId, filename);
        assertTrue(rmCalled.contains(blobPath));
    }

    @Test
    public void testRemoveFileNotFound() {
        String repoId = "foo/bar";
        String filename = "model.gguf";
        String notFound = null;
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.pathFromModel(repoId, filename)).thenReturn(null);

        // Should not throw even if file not found
        assertDoesNotThrow(() -> ModelDownload.remove(repoId, filename));
    }

    @Test
    public void testRemoveRepo() {
        String repoId = "foo/bar";
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.pathFromModel(repoId, "")).thenReturn(null);
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.pathFromRepo(repoId)).thenReturn("/repo/" + repoId);
        // Capture removal
        List<String> rmTree = new ArrayList<>();
        ModelDownload.setRmtreeCallback(p -> {
            rmTree.add(p);
            return null;
        });

        String ret = ModelDownload.remove(repoId, "");
        assertTrue(ret.startsWith("/repo/"));
    }

    @Test
    public void testRemoveRepoNone() {
        String repoId = "foo/bar";
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.pathFromModel(repoId, "")).thenReturn(null);
        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.pathFromRepo(repoId)).thenReturn("");
        ModelDownload.setRmtreeCallback(p -> null);

        assertEquals("", ModelDownload.remove(repoId, ""));
    }
}