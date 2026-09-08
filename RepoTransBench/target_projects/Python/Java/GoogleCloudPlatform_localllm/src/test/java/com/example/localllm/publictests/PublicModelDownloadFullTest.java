package com.example.localllm.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

public class PublicModelDownloadFullTest {

    @Test
    public void testPublicDefaultFilenameValid() {
        Mockito.mockStatic(ModelFiles.class).when(ModelFiles::getDEFAULT_FILE_EXT).thenReturn("gguf");
        String repoId = "OtherAuthor/my-cool-model-884";
        String result = ModelDownload.defaultFilename(repoId);
        assertEquals("my-cool-model-884.Q4_K_M.gguf", result);
    }

    @Test
    public void testPublicDownloadCallsHfHubDownload() {
        HfHubDownloadWrapper hfHubDownload = Mockito.mock(HfHubDownloadWrapper.class);
        Mockito.when(hfHubDownload.hfHubDownload("repoX", "modelFile.bin")).thenReturn("output_path");
        assertEquals("output_path", ModelDownload.download("repoX", "modelFile.bin", hfHubDownload));
        Mockito.verify(hfHubDownload).hfHubDownload("repoX", "modelFile.bin");
    }

    @Test
    public void testPublicRemoveFile() {
        String repoId = "baz/bar";
        String filename = "anothermodel.gguf";
        String blobPath = "/tmp/anothermodel.gguf";

        Mockito.mockStatic(ModelFiles.class).when(() -> ModelFiles.pathFromModel(repoId, filename)).thenReturn(blobPath);
        // Simulate os.remove with a callback appending the path
        final java.util.List<String> rmCalled = new java.util.ArrayList<>();
        ModelDownload.setRemoveCallback(s -> rmCalled.add(s));

        ModelDownload.remove(repoId, filename);
        assertTrue(rmCalled.stream().allMatch(p -> p.contains(blobPath)));
    }
}