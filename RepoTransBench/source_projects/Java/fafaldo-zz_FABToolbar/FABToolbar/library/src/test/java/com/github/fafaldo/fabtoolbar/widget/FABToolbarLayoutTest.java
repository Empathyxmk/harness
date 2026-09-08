package com.github.fafaldo.fabtoolbar.widget;

import android.content.Context;
import android.content.res.TypedArray;
import android.util.AttributeSet;
import android.view.View;
import android.widget.RelativeLayout;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class FABToolbarLayoutTest {

    private Context mockContext;
    private AttributeSet mockAttrs;
    private TypedArray mockTypedArray;

    @Before
    public void setup() {
        mockContext = mock(Context.class);
        mockAttrs = mock(AttributeSet.class);
        mockTypedArray = mock(TypedArray.class);

        // Setup some basic mock values returned
        when(mockContext.obtainStyledAttributes(any(AttributeSet.class), any(int[].class)))
                .thenReturn(mockTypedArray);

        when(mockTypedArray.getInt(anyInt(), anyInt())).thenReturn(500);
        when(mockTypedArray.getDimensionPixelSize(anyInt(), anyInt())).thenReturn(20);
        when(mockTypedArray.getFloat(anyInt(), anyFloat())).thenReturn(0.42f);
        when(mockTypedArray.getResourceId(anyInt(), anyInt())).thenReturn(-1);
        when(mockTypedArray.getBoolean(anyInt(), anyBoolean())).thenReturn(true);
    }

    @Test
    public void testConstructorsAndParseAttrs() {
        // with Context only
        FABToolbarLayout layout1 = new FABToolbarLayout(mockContext);
        assertNotNull(layout1);

        // with Context + AttributeSet
        FABToolbarLayout layout2 = new FABToolbarLayout(mockContext, mockAttrs);
        assertNotNull(layout2);

        // with Context + AttributeSet + defStyleAttr
        FABToolbarLayout layout3 = new FABToolbarLayout(mockContext, mockAttrs, 0);
        assertNotNull(layout3);
    }

    @Test
    public void testParseAttrsFallbacks() {
        // will call parseAttrs
        new FABToolbarLayout(mockContext, mockAttrs);
        verify(mockContext, atLeastOnce()).obtainStyledAttributes(any(AttributeSet.class), any(int[].class));
        verify(mockTypedArray, atLeastOnce()).recycle();
    }
}