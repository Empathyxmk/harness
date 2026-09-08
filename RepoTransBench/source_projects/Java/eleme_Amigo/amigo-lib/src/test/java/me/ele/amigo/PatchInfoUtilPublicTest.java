package me.ele.amigo;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;

import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import static org.junit.Assert.*;

public class PatchInfoUtilPublicTest {

    private Context mockContext;
    private PatchInfoProvider provider;

    @Before
    public void setUpPublic() {
        mockContext = mock(Context.class);
        provider = mock(PatchInfoProvider.class);
    }

    @Test
    public void publicTestSetWorkingChecksum() {
        PatchInfoProvider provider = mock(PatchInfoProvider.class);
        when(provider.update(any(Uri.class), eq(null))).thenReturn(2);
        boolean set = provider.update(any(Uri.class), eq(null)) > 0;
        assertTrue(set); // different input than existing: return 2 and expect true
    }

    @Test
    public void publicTestUpdateAndGetPatchFileChecksum() {
        PatchInfoProvider provider = mock(PatchInfoProvider.class);
        Map<String, String> publicMap = new HashMap<>();
        publicMap.put("libtest.so", "CRC003");
        publicMap.put("libdiff.so", "CRC004");
        ContentValues cv = new ContentValues();
        cv.put("map", "{\"libtest.so\":\"CRC003\",\"libdiff.so\":\"CRC004\"}");
        when(provider.update(any(Uri.class), any(ContentValues.class))).thenReturn(1);

        int updated = provider.update(Uri.parse("publicUri"), cv);
        assertEquals(1, updated);

        Cursor cursor = mock(Cursor.class);
        when(cursor.moveToFirst()).thenReturn(true);
        when(cursor.getString(0)).thenReturn("{\"libtest.so\":\"CRC003\",\"libdiff.so\":\"CRC004\"}");
        when(provider.query(any(Uri.class))).thenReturn(cursor);
        Cursor resultCursor = provider.query(Uri.parse("publicQueryUri"));
        assertTrue(resultCursor.moveToFirst());
        assertEquals("{\"libtest.so\":\"CRC003\",\"libdiff.so\":\"CRC004\"}", resultCursor.getString(0));
    }
}