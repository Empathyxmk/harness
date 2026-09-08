package xzr.hkf;

import android.app.Activity;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class WorkerPublicTest {

    Activity mockActivity;
    Worker worker;

    @Before
    public void setUp() {
        mockActivity = mock(Activity.class);
        when(mockActivity.getFilesDir()).thenReturn(new File(System.getProperty("java.io.tmpdir"), "workerpublictest"));
        worker = spy(new Worker(mockActivity));
        worker.uri = null;
    }

    @Test
    public void testRootAvailable_True_Public() throws Exception {
        doReturn("root otheruser").when(worker).runWithNewProcessReturn(true, "id");
        assertTrue(worker.rootAvailable());
    }

    @Test
    public void testRootAvailable_False_Public() throws Exception {
        doReturn(null).when(worker).runWithNewProcessReturn(true, "id");
        assertFalse(worker.rootAvailable());
    }

    @Test
    public void testCopy_Throws_Public() throws Exception {
        doThrow(new IOException("fail again")).when(mockActivity).getContentResolver();
        try {
            worker.copy();
            fail("Should throw exception");
        } catch (Exception e) {
            // expected
        }
    }

    @Test
    public void testGetBinary_NotExist_Public() throws Exception {
        doNothing().when(worker).runWithNewProcessNoReturn(anyBoolean(), anyString());
        worker.file_path = System.getProperty("java.io.tmpdir") + "/definitely_missing.zip";
        worker.binary_path = System.getProperty("java.io.tmpdir") + "/definitely_missing-binary";
        try {
            worker.getBinary();
            fail("Should throw IOException");
        } catch (IOException e) {
            // expected
        }
    }

    @Test
    public void testPatch_AssetsUtilThrows_Public() throws Exception {
        doThrow(new IOException("fail2")).when(worker).runWithNewProcessNoReturn(anyBoolean(), anyString());
        try {
            worker.patch();
        } catch (IOException e) {
            // expected
        }
    }

    @Test
    public void testFlash_Throws_Public() throws Exception {
        doThrow(new IOException("fail3")).when(worker).runWithNewProcessReturn(anyBoolean(), anyString());
        try {
            worker.flash(mockActivity);
            fail("Should throw IOException");
        } catch (IOException e) {
            // expected
        }
    }
}