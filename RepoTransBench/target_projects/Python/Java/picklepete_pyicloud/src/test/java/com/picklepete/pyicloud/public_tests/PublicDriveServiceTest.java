package com.picklepete.pyicloud.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.picklepete.pyicloud.services.PyiCloudServiceMock;

import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;

public class PublicDriveServiceTest {

    private PyiCloudServiceMock service;

    @BeforeEach
    public void setUp() {
        service = new PyiCloudServiceMock(PyiCloudServiceMock.AUTHENTICATED_USER, PyiCloudServiceMock.VALID_PASSWORD);
    }

    @Test
    public void testRootPublic() {
        var drive = service.getDrive();
        // Use set to compare unordered contents
        Set<String> rootChildren = new HashSet<>(drive.dir());
        Set<String> expected = new HashSet<>(Arrays.asList("Preview", "Keynote", "Pages", "pyiCloud", "Numbers"));
        assertEquals(expected, rootChildren);
        assertEquals("", drive.getName());
        assertEquals("folder", drive.getType());
        assertNull(drive.getSize());
    }

    @Test
    public void testFolderAppPublic() {
        var folder = service.getDrive().get("Keynote");
        assertEquals("Keynote", folder.getName());
        assertEquals("app_library", folder.getType());
        assertNull(folder.getSize());
        Exception ex = assertThrows(KeyException.class, () -> folder.dir());
        assertTrue(ex.getMessage().contains("No items in folder, status: ID_INVALID"));
    }

    @Test
    public void testFolderNotExistsPublic() {
        Exception exception = assertThrows(KeyException.class, () ->
            service.getDrive().get("ghost_folder")
        );
        assertTrue(exception.getMessage().contains("No child named 'ghost_folder' exists"));
    }

    @Test
    public void testFolderPublic() {
        var folder = service.getDrive().get("Pages");
        assertEquals("Pages", folder.getName());
        assertEquals("folder", folder.getType());
        assertNull(folder.getSize());
        Exception ex = assertThrows(KeyException.class, () -> folder.dir());
        assertTrue(ex.getMessage().contains("No items in folder, status: ID_INVALID"));
    }

    @Test
    public void testSubfolderPublic() {
        var folder = service.getDrive().get("pyiCloud").get("Test");
        var fileList = folder.dir();
        // Reverse expected list for assertion
        var expected = Arrays.asList("Scanned document 1.pdf", "Document scanné 2.pdf");
        java.util.Collections.reverse(fileList);
        assertEquals(expected, fileList);
        assertEquals("Test", folder.getName());
        assertEquals("folder", folder.getType());
    }

    @Test
    public void testSubfolderFilePublic() {
        var folder = service.getDrive().get("pyiCloud").get("Test");
        var fileTest = folder.get("Document scanné 2.pdf");
        assertEquals("Document scanné 2.pdf", fileTest.getName());
        assertEquals("file", fileTest.getType());
        assertNotEquals(Integer.valueOf(21644358), fileTest.getSize());
        assertTrue(fileTest.getDateChanged().toString().startsWith("2020-"));
        assertNull(fileTest.dir());
    }

    @Test
    public void testFileOpenPublic() throws Exception {
        var fileTest = service.getDrive().get("pyiCloud").get("Test").get("Document scanné 2.pdf");
        try (var response = fileTest.open(true)) {
            assertNotNull(response.getRaw());
        }
    }
}