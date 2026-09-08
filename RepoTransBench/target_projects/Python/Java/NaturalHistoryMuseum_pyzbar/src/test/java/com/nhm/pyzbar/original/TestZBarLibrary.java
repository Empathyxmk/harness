package com.nhm.pyzbar.original;

import com.nhm.pyzbar.zbar_library.ZBarLibrary;
import org.junit.jupiter.api.*;
import org.mockito.MockedStatic;
import org.mockito.Mockito;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class TestZBarLibrary {

    @BeforeEach
    void setUp() {
        // setUp for mocks if needed
    }

    @Test
    void testFoundNonWindows() {
        try (MockedStatic<ZBarLibrary> mocked = Mockito.mockStatic(ZBarLibrary.class, Mockito.CALLS_REAL_METHODS)) {
            mocked.when(ZBarLibrary::getSystem).thenReturn("Not windows");
            mocked.when(() -> ZBarLibrary.loadLibraryByName("zbar")).thenReturn("libzbar.so");
            Object[] result = ZBarLibrary.load();
            assertEquals("libzbar.so", result[0]);
            // No dependencies on Windows
            assertEquals(0, ((List<?>) result[1]).size());
        }
    }

    @Test
    void testNotFoundNonWindows() {
        try (MockedStatic<ZBarLibrary> mocked = Mockito.mockStatic(ZBarLibrary.class, Mockito.CALLS_REAL_METHODS)) {
            mocked.when(ZBarLibrary::getSystem).thenReturn("Not windows");
            mocked.when(() -> ZBarLibrary.loadLibraryByName("zbar")).thenReturn(null);
            assertThrows(IllegalStateException.class, ZBarLibrary::load);
        }
    }

    @Test
    void testFoundWindows() {
        try (MockedStatic<ZBarLibrary> mocked = Mockito.mockStatic(ZBarLibrary.class, Mockito.CALLS_REAL_METHODS)) {
            mocked.when(ZBarLibrary::getSystem).thenReturn("Windows");
            mocked.when(() -> ZBarLibrary._windowsDllNames()).thenReturn(new String[]{"dll fname", "dependency fname"});
            mocked.when(() -> ZBarLibrary.loadLibraryByName("dll fname")).thenReturn("dllresult");
            mocked.when(() -> ZBarLibrary.loadLibraryByName("dependency fname")).thenReturn("depresult");
            Object[] result = ZBarLibrary.load();
            assertEquals("dllresult", result[0]);
            assertTrue(((List<?>) result[1]).contains("depresult"));
        }
    }

    @Test
    void testNotFoundWindows() {
        try (MockedStatic<ZBarLibrary> mocked = Mockito.mockStatic(ZBarLibrary.class, Mockito.CALLS_REAL_METHODS)) {
            mocked.when(ZBarLibrary::getSystem).thenReturn("Windows");
            mocked.when(() -> ZBarLibrary.loadLibraryByName(Mockito.any())).thenThrow(new RuntimeException("Not found"));
            assertThrows(RuntimeException.class, ZBarLibrary::load);
        }
    }
}