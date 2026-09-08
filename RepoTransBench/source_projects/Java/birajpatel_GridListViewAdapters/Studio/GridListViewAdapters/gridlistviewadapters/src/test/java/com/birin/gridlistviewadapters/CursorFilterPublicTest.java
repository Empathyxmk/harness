package com.birin.gridlistviewadapters;

import android.database.Cursor;
import android.widget.Filter;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.mockito.Mockito.*;

/**
 * Public test for CursorFilter using different input data/values.
 */
class CursorFilterPublicTest {
    CursorFilter.CursorFilterClient client;
    Cursor cursor;

    @BeforeEach
    void setUp() {
        client = mock(CursorFilter.CursorFilterClient.class);
        cursor = mock(Cursor.class);
    }

    @Test
    void testConvertResultToStringPublic() {
        when(client.convertToString(cursor)).thenReturn("publicTest");
        CursorFilter filter = new CursorFilter(client);
        Assertions.assertEquals("publicTest", filter.convertResultToString(cursor));
    }

    @Test
    void testPerformFilteringWithCursorPublic() {
        when(client.runQueryOnBackgroundThread("xyz")).thenReturn(cursor);
        when(cursor.getCount()).thenReturn(7);
        CursorFilter filter = new CursorFilter(client);
        Filter.FilterResults results = filter.performFiltering("xyz");

        Assertions.assertEquals(7, results.count);
        Assertions.assertEquals(cursor, results.values);
    }

    @Test
    void testPerformFilteringNullCursorPublic() {
        when(client.runQueryOnBackgroundThread("nullcase")).thenReturn(null);
        CursorFilter filter = new CursorFilter(client);
        Filter.FilterResults results = filter.performFiltering("nullcase");
        Assertions.assertEquals(0, results.count);
        Assertions.assertNull(results.values);
    }

    @Test
    void testPublishResultsWithNonNullCursorDifferentFromOldPublic() {
        Cursor oldCursor = mock(Cursor.class);
        Filter.FilterResults results = new Filter.FilterResults();
        results.values = cursor;

        when(client.getCursor()).thenReturn(oldCursor);
        CursorFilter filter = new CursorFilter(client);
        filter.publishResults("z", results);

        verify(client).changeCursor(cursor);
    }

    @Test
    void testPublishResultsWithNullValuesPublic() {
        Filter.FilterResults results = new Filter.FilterResults();
        results.values = null;
        when(client.getCursor()).thenReturn(cursor);
        CursorFilter filter = new CursorFilter(client);
        filter.publishResults("z", results);

        // Should *not* call changeCursor
        verify(client, never()).changeCursor(any());
    }

    @Test
    void testPublishResultsWithSameCursorPublic() {
        Filter.FilterResults results = new Filter.FilterResults();
        results.values = cursor;
        when(client.getCursor()).thenReturn(cursor);
        CursorFilter filter = new CursorFilter(client);
        filter.publishResults("z", results);

        verify(client, never()).changeCursor(any());
    }
}