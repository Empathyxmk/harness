package com.angeloc.s3pitrestore.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.nio.file.*;
import java.util.*;

public class PublicS3PitRestoreUnittestTest {

    // Simulates TestS3PitRestore class and generate_tree for public test
    static class DummyTestS3PitRestore {
        public void generate_tree(String outputDir, List<String> folderNames) throws Exception {
            File dir = new File(outputDir);
            if (!dir.exists()) {
                dir.mkdirs();
            }
            for (String folder : folderNames) {
                File subDir = new File(dir, folder);
                subDir.mkdirs();
                File file = new File(subDir, "dummy.txt");
                try (FileWriter fw = new FileWriter(file)) {
                    fw.write("dummy");
                }
            }
        }
    }

    @Test
    public void testTestS3PitRestoreGenerateTreePublic() throws Exception {
        // Use different directory / folder names compared to original
        Path tmpPath = Files.createTempDirectory("s3pitrestoretest-public");
        File genDir = tmpPath.resolve("treepub").toFile();
        genDir.mkdirs();

        DummyTestS3PitRestore testObj = new DummyTestS3PitRestore();
        List<String> folderNames = Arrays.asList("foo", "bar", "baz");
        testObj.generate_tree(genDir.getAbsolutePath(), folderNames);

        File[] folders = genDir.listFiles(File::isDirectory);
        assertNotNull(folders, "Subdirectories do not exist");
        assertEquals(3, folders.length, "Should have three subdirectories");
        for (File folder : folders) {
            File[] files = folder.listFiles(File::isFile);
            assertNotNull(files, "Each subdirectory should have files");
            assertEquals(1, files.length, "Each subdirectory should have one file");
        }
    }
}