package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.picklepete.pyicloud.services.PyiCloudServiceMock;

public class DriveServiceTest {

    private PyiCloudServiceMock service;

    @BeforeEach
    public void setUp() {
        service = new PyiCloudServiceMock(PyiCloudServiceMock.AUTHENTICATED_USER, PyiCloudServiceMock.VALID_PASSWORD);
    }

    @Test
    public void testRoot() {
        var drive = service.getDrive();
        assertEquals("", drive.getName());
        assertEquals("folder", drive.getType());
        assertNull(drive.getSize());
        assertNull(drive.getDateChanged());
        assertNull(drive.getDateModified());
        assertNull(drive.getDateLastOpen());
        assertArrayEquals(
                new String[] {"Keynote", "Numbers", "Pages", "Preview", "pyiCloud"},
                drive.dir().toArray(new String[0]));
    }

    @Test
    public void testFolderApp() {
        var folder = service.getDrive().get("Preview");
        assertEquals("Preview", folder.getName());
        assertEquals("app_library", folder.getType());
        assertNull(folder.getSize());
        assertNull(folder.getDateChanged());
        assertNull(folder.getDateModified());
        assertNull(folder.getDateLastOpen());
        Exception exception = assertThrows(KeyException.class, () -> folder.dir());
        assertTrue(exception.getMessage().contains("No items in folder, status: ID_INVALID"));
    }

    @Test
    public void testFolderNotExists() {
        Exception exception = assertThrows(KeyException.class, () ->
            service.getDrive().get("not_exists")
        );
        assertTrue(exception.getMessage().contains("No child named 'not_exists' exists"));
    }

    @Test
    public void testFolder() {
        var folder = service.getDrive().get("pyiCloud");
        assertEquals("pyiCloud", folder.getName());
        assertEquals("folder", folder.getType());
        assertNull(folder.getSize());
        assertNull(folder.getDateChanged());
        assertNull(folder.getDateModified());
        assertNull(folder.getDateLastOpen());
        assertArrayEquals(
                new String[] {"Test"},
                folder.dir().toArray(new String[0]));
    }

    @Test
    public void testSubfolder() {
        var folder = service.getDrive().get("pyiCloud").get("Test");
        assertEquals("Test", folder.getName());
        assertEquals("folder", folder.getType());
        assertNull(folder.getSize());
        assertNull(folder.getDateChanged());
        assertNull(folder.getDateModified());
        assertNull(folder.getDateLastOpen());
        assertArrayEquals(
                new String[] {"Document scanné 2.pdf", "Scanned document 1.pdf"},
                folder.dir().toArray(new String[0]));
    }

    @Test
    public void testSubfolderFile() {
        var folder = service.getDrive().get("pyiCloud").get("Test");
        var fileTest = folder.get("Scanned document 1.pdf");
        assertEquals("Scanned document 1.pdf", fileTest.getName());
        assertEquals("file", fileTest.getType());
        assertEquals(Integer.valueOf(21644358), fileTest.getSize());
        assertEquals("2020-05-03 00:16:17", fileTest.getDateChanged().toString());
        assertEquals("2020-05-03 00:15:17", fileTest.getDateModified().toString());
        assertEquals("2020-05-03 00:24:25", fileTest.getDateLastOpen().toString());
        assertNull(fileTest.dir());
    }

    @Test
    public void testFileOpen() throws Exception {
        var fileTest = service.getDrive().get("pyiCloud").get("Test").get("Scanned document 1.pdf");
        try (var response = fileTest.open(true)) {
            assertNotNull(response.getRaw());
        }
    }
}