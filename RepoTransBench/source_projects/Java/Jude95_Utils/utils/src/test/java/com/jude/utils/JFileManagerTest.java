package com.jude.utils;

import org.junit.jupiter.api.*;

import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

class JFileManagerTest {

    enum Dir { TEST }

    private static Path tempDir;

    static class DummyContext extends android.test.mock.MockContext {
        @Override
        public java.io.File getFilesDir() {
            return tempDir.toFile();
        }
    }

    static class TestObj implements Serializable {
        int x;
        public TestObj(int x) { this.x = x; }
    }

    @BeforeAll
    static void setupTmpDir() throws Exception {
        tempDir = Files.createTempDirectory("jfilemanager_test");
    }

    @AfterAll
    static void cleanTmpDir() throws Exception {
        if(tempDir != null) {
            Files.walk(tempDir)
                    .sorted((a, b) -> b.compareTo(a))
                    .forEach(p -> p.toFile().delete());
        }
    }

    @Test
    void testInitAndGetFolder() {
        JFileManager mgr = JFileManager.getInstance();
        mgr.init(new DummyContext(), Dir.values());
        JFileManager.Folder folder = mgr.getFolder(Dir.TEST);
        assertNotNull(folder);
        assertTrue(folder.getFile().exists());
    }

    @Test
    void testWriteAndReadString() {
        JFileManager mgr = JFileManager.getInstance();
        mgr.init(new DummyContext(), Dir.values());
        JFileManager.Folder folder = mgr.getFolder(Dir.TEST);

        folder.writeStringToFile("hello world", "string.txt");
        String read = folder.readStringFromFile("string.txt");
        assertEquals("hello world", read);

        assertNull(folder.readStringFromFile("not_exist.txt"));
    }

    @Test
    void testWriteAndReadObject() throws Exception {
        JFileManager mgr = JFileManager.getInstance();
        mgr.init(new DummyContext(), Dir.values());
        JFileManager.Folder folder = mgr.getFolder(Dir.TEST);

        TestObj obj = new TestObj(1234);
        folder.writeObjectToFile(obj, "obj.bin");

        TestObj read = folder.readObjectFromFile("obj.bin");
        assertEquals(1234, read.x);

        // Remove file, make sure readObjectFromFile throws
        folder.deleteChild("obj.bin");
        assertThrows(Exception.class, () -> folder.readObjectFromFile("obj.bin"));
    }

    @Test
    void testListAndDeleteChild() {
        JFileManager mgr = JFileManager.getInstance();
        mgr.init(new DummyContext(), Dir.values());
        JFileManager.Folder folder = mgr.getFolder(Dir.TEST);

        folder.writeStringToFile("data1", "f1.txt");
        folder.writeStringToFile("data2", "f2.txt");
        assertEquals(2, folder.listChildFile().length);

        folder.deleteChild("f1.txt");
        assertEquals(1, folder.listChildFile().length);
    }

    @Test
    void testClearAllData() {
        JFileManager mgr = JFileManager.getInstance();
        mgr.init(new DummyContext(), Dir.values());
        JFileManager.Folder folder = mgr.getFolder(Dir.TEST);
        folder.writeStringToFile("t", "f.txt");
        assertTrue(folder.getChildFile("f.txt").exists());
        mgr.clearAllData();
        assertFalse(folder.getChildFile("f.txt").exists());
    }
}