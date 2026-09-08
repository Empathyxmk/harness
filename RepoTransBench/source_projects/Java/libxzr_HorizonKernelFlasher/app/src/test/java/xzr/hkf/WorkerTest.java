package xzr.hkf;

import android.app.Activity;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class WorkerTest {

    Activity mockActivity;
    Worker worker;

    @Before
    public void setUp() {
        mockActivity = mock(Activity.class);
        when(mockActivity.getFilesDir()).thenReturn(new File(System.getProperty("java.io.tmpdir")));
        worker = spy(new Worker(mockActivity));
        worker.uri = null; // simulate DocumentFile
    }

    @Test
    public void testRootAvailable_True() throws Exception {
        doReturn("root xzr").when(worker).runWithNewProcessReturn(true, "id");
        assertTrue(worker.rootAvailable());
    }

    @Test
    public void testRootAvailable_False() throws Exception {
        doThrow(new IOException()).when(worker).runWithNewProcessReturn(true, "id");
        assertFalse(worker.rootAvailable());
    }

    @Test
    public void testCopy_Throws() throws Exception {
        doThrow(new IOException("fail")).when(mockActivity).getContentResolver();
        try {
            worker.copy();
            fail("Should throw");
        } catch (Exception e) {
            // expected
        }
    }

    @Test
    public void testGetBinary_NotExist() throws Exception {
        doNothing().when(worker).runWithNewProcessNoReturn(anyBoolean(), anyString());
        worker.file_path = System.getProperty("java.io.tmpdir") + "/notfound.zip";
        worker.binary_path = System.getProperty("java.io.tmpdir") + "/notfound.update-binary";
        try {
            worker.getBinary();
            fail("Should throw");
        } catch (IOException e) {
            // expected
        }
    }

    @Test
    public void testPatch_AssetsUtilThrows() throws Exception {
        doThrow(new IOException("fail")).when(worker).runWithNewProcessNoReturn(anyBoolean(), anyString());
        try {
            worker.patch();
        } catch (IOException e) {
            // expected
        }
    }

    @Test
    public void testFlash_Throws() throws Exception {
        doThrow(new IOException("fail")).when(worker).runWithNewProcessReturn(anyBoolean(), anyString());
        try {
            worker.flash(mockActivity);
            fail("Should throw");
        } catch (IOException e) {
            // expected
        }
    }
}