package org.jak_linux.dns66;

import org.junit.*;
import android.content.Context;
import static org.mockito.Mockito.*;
import java.io.*;

public class FileHelperMinimalTest {

    @Test
    public void testOpenRead_fileFound() throws Exception {
        Context ctx = mock(Context.class);
        InputStream is = new ByteArrayInputStream("abc".getBytes());
        when(ctx.openFileInput(anyString())).thenReturn(is);
        InputStream result = FileHelper.openRead(ctx, "file.txt");
        Assert.assertEquals('a', result.read());
    }

    @Test
    public void testOpenRead_fileNotFoundFallsBackToAssets() throws Exception {
        Context ctx = mock(Context.class);
        when(ctx.openFileInput(anyString())).thenThrow(new FileNotFoundException());
        InputStream ais = new ByteArrayInputStream("xyz".getBytes());
        when(ctx.getAssets().open(anyString())).thenReturn(ais);
        InputStream result = FileHelper.openRead(ctx, "file.txt");
        Assert.assertEquals('x', result.read());
    }
}