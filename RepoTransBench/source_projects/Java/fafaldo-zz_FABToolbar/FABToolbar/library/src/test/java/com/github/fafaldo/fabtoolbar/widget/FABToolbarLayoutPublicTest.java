package com.github.fafaldo.fabtoolbar.widget;

import android.content.Context;
import android.content.res.TypedArray;
import android.util.AttributeSet;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class FABToolbarLayoutPublicTest {

    private Context mockContext;
    private AttributeSet mockAttrs;
    private TypedArray mockTypedArray;

    @Before
    public void setup() {
        mockContext = mock(Context.class);
        mockAttrs = mock(AttributeSet.class);
        mockTypedArray = mock(TypedArray.class);

        // Use different mock return values than in the original test
        when(mockContext.obtainStyledAttributes(any(AttributeSet.class), any(int[].class)))
                .thenReturn(mockTypedArray);

        when(mockTypedArray.getInt(anyInt(), anyInt())).thenReturn(888);
        when(mockTypedArray.getDimensionPixelSize(anyInt(), anyInt())).thenReturn(50);
        when(mockTypedArray.getFloat(anyInt(), anyFloat())).thenReturn(0.88f);
        when(mockTypedArray.getResourceId(anyInt(), anyInt())).thenReturn(42);
        when(mockTypedArray.getBoolean(anyInt(), anyBoolean())).thenReturn(false);
    }

    @Test
    public void testConstructorsWithOtherValues() {
        // Context constructor
        FABToolbarLayout layout1 = new FABToolbarLayout(mockContext);
        assertNotNull(layout1);

        // Context + AttributeSet constructor
        FABToolbarLayout layout2 = new FABToolbarLayout(mockContext, mockAttrs);
        assertNotNull(layout2);

        // Context + AttributeSet + defStyleAttr constructor
        FABToolbarLayout layout3 = new FABToolbarLayout(mockContext, mockAttrs, 1);
        assertNotNull(layout3);
    }

    @Test
    public void testParseAttrsPublic() {
        new FABToolbarLayout(mockContext, mockAttrs);
        verify(mockContext, atLeastOnce()).obtainStyledAttributes(any(AttributeSet.class), any(int[].class));
        verify(mockTypedArray, atLeastOnce()).recycle();
    }
}