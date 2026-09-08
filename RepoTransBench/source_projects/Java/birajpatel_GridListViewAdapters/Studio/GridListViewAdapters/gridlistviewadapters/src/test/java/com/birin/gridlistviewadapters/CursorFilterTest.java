package com.birin.gridlistviewadapters;

import android.database.Cursor;
import android.widget.Filter;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.mockito.Mockito.*;

class CursorFilterTest {
    CursorFilter.CursorFilterClient client;
    Cursor cursor;

    @BeforeEach
    void setUp() {
        client = mock(CursorFilter.CursorFilterClient.class);
        cursor = mock(Cursor.class);
    }

    @Test
    void testConvertResultToString() {
        when(client.convertToString(cursor)).thenReturn("test");
        CursorFilter filter = new CursorFilter(client);
        Assertions.assertEquals("test", filter.convertResultToString(cursor));
    }

    @Test
    void testPerformFilteringWithCursor() {
        when(client.runQueryOnBackgroundThread("abc")).thenReturn(cursor);
        when(cursor.getCount()).thenReturn(5);
        CursorFilter filter = new CursorFilter(client);
        Filter.FilterResults results = filter.performFiltering("abc");

        Assertions.assertEquals(5, results.count);
        Assertions.assertEquals(cursor, results.values);
    }

    @Test
    void testPerformFilteringNullCursor() {
        when(client.runQueryOnBackgroundThread("none")).thenReturn(null);
        CursorFilter filter = new CursorFilter(client);
        Filter.FilterResults results = filter.performFiltering("none");
        Assertions.assertEquals(0, results.count);
        Assertions.assertNull(results.values);
    }

    @Test
    void testPublishResultsWithNonNullCursorDifferentFromOld() {
        Cursor oldCursor = mock(Cursor.class);
        Filter.FilterResults results = new Filter.FilterResults();
        results.values = cursor;

        when(client.getCursor()).thenReturn(oldCursor);
        CursorFilter filter = new CursorFilter(client);
        filter.publishResults("c", results);

        verify(client).changeCursor(cursor);
    }

    @Test
    void testPublishResultsWithNullValues() {
        Filter.FilterResults results = new Filter.FilterResults();
        results.values = null;
        when(client.getCursor()).thenReturn(cursor);
        CursorFilter filter = new CursorFilter(client);
        filter.publishResults("c", results);

        // Should *not* call changeCursor
        verify(client, never()).changeCursor(any());
    }

    @Test
    void testPublishResultsWithSameCursor() {
        Filter.FilterResults results = new Filter.FilterResults();
        results.values = cursor;
        when(client.getCursor()).thenReturn(cursor);
        CursorFilter filter = new CursorFilter(client);
        filter.publishResults("c", results);

        verify(client, never()).changeCursor(any());
    }
}