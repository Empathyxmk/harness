package xzr.hkf.utils;

import android.content.Context;
import android.content.res.AssetManager;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.io.*;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AssetsUtilTest {

    Context context;
    AssetManager assetManager;

    @Before
    public void setUp() {
        context = mock(Context.class);
        assetManager = mock(AssetManager.class);
        when(context.getAssets()).thenReturn(assetManager);
    }

    @Test
    public void testExportFiles_Directory() throws Exception {
        // directory with two files
        when(assetManager.list("src")).thenReturn(new String[]{"f1", "f2"});
        when(assetManager.list("src/f1")).thenReturn(new String[0]);
        when(assetManager.list("src/f2")).thenReturn(new String[0]);
        when(assetManager.open(anyString())).thenAnswer(invocation -> new ByteArrayInputStream("content".getBytes()));
        File tempDir = new File(System.getProperty("java.io.tmpdir"), "assetsutiltest");
        tempDir.mkdirs();

        AssetsUtil.exportFiles(context, "src", tempDir.getAbsolutePath());
        assertTrue(tempDir.exists());
    }

    @Test
    public void testExportFiles_EmptyFile() throws Exception {
        // treat as a file directly
        when(assetManager.list("foo")).thenReturn(new String[0]);
        InputStream is = new ByteArrayInputStream("ok".getBytes());
        when(assetManager.open("foo")).thenReturn(is);
        File tempFile = File.createTempFile("AssetsUtilTest", ".tmp");
        AssetsUtil.exportFiles(context, "foo", tempFile.getAbsolutePath());
        assertEquals(tempFile.length(), 2);
        tempFile.delete();
    }

    @Test(expected = IOException.class)
    public void testExportFiles_IOException() throws Exception {
        when(assetManager.list("bad")).thenThrow(new IOException("failtest"));
        AssetsUtil.exportFiles(context, "bad", "/tmp/notused");
    }
}