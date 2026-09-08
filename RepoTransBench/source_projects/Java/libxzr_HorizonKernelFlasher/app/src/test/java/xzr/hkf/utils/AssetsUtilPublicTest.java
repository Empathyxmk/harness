package xzr.hkf.utils;

import android.content.Context;
import android.content.res.AssetManager;
import org.junit.Before;
import org.junit.Test;

import java.io.*;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AssetsUtilPublicTest {

    Context context;
    AssetManager assetManager;

    @Before
    public void setUp() {
        context = mock(Context.class);
        assetManager = mock(AssetManager.class);
        when(context.getAssets()).thenReturn(assetManager);
    }

    @Test
    public void testExportFiles_Directory_Public() throws Exception {
        // directory with three files (new test data)
        when(assetManager.list("pub")).thenReturn(new String[]{"a", "b", "c"});
        when(assetManager.list("pub/a")).thenReturn(new String[0]);
        when(assetManager.list("pub/b")).thenReturn(new String[0]);
        when(assetManager.list("pub/c")).thenReturn(new String[0]);
        when(assetManager.open(anyString())).thenAnswer(invocation -> new ByteArrayInputStream("pubdata".getBytes()));
        File tempDir = new File(System.getProperty("java.io.tmpdir"), "assetsutilpublictest");
        tempDir.mkdirs();

        AssetsUtil.exportFiles(context, "pub", tempDir.getAbsolutePath());
        assertTrue(tempDir.exists());
    }

    @Test
    public void testExportFiles_EmptyFile_Public() throws Exception {
        // use a different asset name and content
        when(assetManager.list("baz")).thenReturn(new String[0]);
        InputStream is = new ByteArrayInputStream("OK".getBytes()); // capital OK for public
        when(assetManager.open("baz")).thenReturn(is);
        File tempFile = File.createTempFile("AssetsUtilPublicTest", ".tmp");
        AssetsUtil.exportFiles(context, "baz", tempFile.getAbsolutePath());
        assertEquals(tempFile.length(), 2);
        tempFile.delete();
    }

    @Test(expected = IOException.class)
    public void testExportFiles_IOException_Public() throws Exception {
        when(assetManager.list("broken")).thenThrow(new IOException("failtest-broken"));
        AssetsUtil.exportFiles(context, "broken", "/tmp/notusedpub");
    }
}