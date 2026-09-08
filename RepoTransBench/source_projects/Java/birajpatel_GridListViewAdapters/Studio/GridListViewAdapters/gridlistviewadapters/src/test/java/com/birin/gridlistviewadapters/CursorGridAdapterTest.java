package com.birin.gridlistviewadapters;

import android.content.Context;
import android.database.Cursor;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FilterQueryProvider;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class CursorGridAdapterTest {

    static class ConcreteCursorGridAdapter extends CursorGridAdapter<Object> {
        public ConcreteCursorGridAdapter(Context context, int totalCardsInRow, Cursor c) {
            super(context, totalCardsInRow, c);
        }
        @Override public View getView(int position, View convertView, ViewGroup parent) { return null; }
        @Override public Card<Object> getNewCard(int cardPositionInRow) { return null; }
    }

    Context mockContext;
    Cursor mockCursor;
    ConcreteCursorGridAdapter adapter;

    @BeforeEach
    void setup() {
        mockContext = mock(Context.class, RETURNS_DEEP_STUBS);
        mockCursor = mock(Cursor.class);
        when(mockContext.getSystemService(anyString())).thenReturn(null);
        // return plausible DisplayMetrics in chained call
        when(mockContext.getResources().getDisplayMetrics().widthPixels).thenReturn(240);
        when(mockContext.getResources().getDisplayMetrics().heightPixels).thenReturn(320);
        when(mockCursor.getCount()).thenReturn(5);

        adapter = new ConcreteCursorGridAdapter(mockContext, 2, mockCursor);
    }

    @Test
    void returnsSameCursorFromGetCursor() {
        assertSame(mockCursor, adapter.getCursor());
    }

    @Test
    void changeCursorClosesOld() {
        Cursor old = mock(Cursor.class);
        adapter.mCursor = old;
        Cursor newCursor = mock(Cursor.class);
        when(newCursor.getCount()).thenReturn(3);

        adapter.changeCursor(newCursor);

        verify(old, times(1)).close();
        assertSame(newCursor, adapter.getCursor());
    }

    @Test
    void swapCursorReturnsNullWhenSame() {
        adapter.mCursor = mockCursor;
        assertNull(adapter.swapCursor(mockCursor));
    }

    @Test
    void swapCursorReturnsOldAndUpdates() {
        Cursor old = mock(Cursor.class);
        Cursor newC = mock(Cursor.class);
        when(newC.getCount()).thenReturn(4);

        adapter.mCursor = old;
        Cursor result = adapter.swapCursor(newC);

        assertSame(old, result);
        assertSame(newC, adapter.getCursor());
    }

    @Test
    void swapCursorToNull() {
        adapter.mCursor = mockCursor;
        Cursor returned = adapter.swapCursor(null);

        assertSame(mockCursor, returned);
        assertNull(adapter.getCursor());
    }

    @Test
    void convertToStringHandlesNull() {
        assertEquals("", adapter.convertToString(null));
    }

    @Test
    void convertToStringHandlesNonNull() {
        Cursor c = mock(Cursor.class);
        when(c.toString()).thenReturn("CURSORSTR");
        assertEquals("CURSORSTR", adapter.convertToString(c));
    }

    @Test
    void runQueryOnBackgroundThread_WithProvider() {
        Cursor cursor = mock(Cursor.class);
        FilterQueryProvider provider = mock(FilterQueryProvider.class);
        when(provider.runQuery("kkk")).thenReturn(cursor);
        adapter.mFilterQueryProvider = provider;
        assertSame(cursor, adapter.runQueryOnBackgroundThread("kkk"));
    }

    @Test
    void runQueryOnBackgroundThread_NoProvider() {
        adapter.mCursor = mockCursor;
        adapter.mFilterQueryProvider = null;
        assertSame(mockCursor, adapter.runQueryOnBackgroundThread("z"));
    }
}