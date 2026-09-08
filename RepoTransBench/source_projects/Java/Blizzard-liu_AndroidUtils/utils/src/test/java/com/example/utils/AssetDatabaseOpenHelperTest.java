package com.example.utils;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import org.junit.Test;
import org.mockito.Mockito;

import java.io.File;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AssetDatabaseOpenHelperTest {
    @Test
    public void testGetDatabaseName() {
        Context ctx = mock(Context.class);
        AssetDatabaseOpenHelper helper = new AssetDatabaseOpenHelper(ctx, "mydb.db");
        assertEquals("mydb.db", helper.getDatabaseName());
    }

    // We're not testing actual database copy/open, but error handling can be checked.
    @Test(expected = RuntimeException.class)
    public void testGetWritableDatabase_ioException() throws Exception {
        Context ctx = mock(Context.class);
        File dbFile = mock(File.class);
        when(ctx.getDatabasePath(anyString())).thenReturn(dbFile);
        when(dbFile.exists()).thenReturn(false);
        // Make context.getAssets().open throw IOException
        AssetDatabaseOpenHelper helper = new AssetDatabaseOpenHelper(ctx, "fail.db");
        doThrow(new java.io.IOException("fail")).when(ctx.getAssets()).open("fail.db");
        helper.getWritableDatabase();
    }
}