package com.fenjuly.mylibrary;

import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
import android.widget.FrameLayout;

import com.nineoldandroids.animation.Animator;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for ToggleExpandLayout.
 * Note: Uses Mockito for mocks, so ensure mockito-core is in the test deps.
 */
public class ToggleExpandLayoutTest {

    private ToggleExpandLayout layout;
    private Context context;

    @Before
    public void setUp() {
        // mock context to avoid Android dependencies
        context = mock(Context.class);
        layout = new ToggleExpandLayout(context);
    }

    @Test
    public void testSetOnToggleTouchListener() {
        ToggleExpandLayout.OnToggleTouchListener listener = mock(ToggleExpandLayout.OnToggleTouchListener.class);
        layout.setOnToggleTouchListener(listener);
        assertNotNull(layout);
    }

    @Test
    public void testOpen_andClose_NoChildren() {
        ToggleExpandLayout.OnToggleTouchListener listener = mock(ToggleExpandLayout.OnToggleTouchListener.class);
        layout.setOnToggleTouchListener(listener);

        // Should not throw error even without children
        layout.open();
        layout.close();
    }

    @Test
    public void testOpen_andClose_WithChildren() {
        // Setup basic children Views
        View child0 = mock(View.class);
        when(child0.getMeasuredWidth()).thenReturn(20);
        when(child0.getMeasuredHeight()).thenReturn(15);

        View child1 = mock(View.class);
        when(child1.getMeasuredWidth()).thenReturn(30);
        when(child1.getMeasuredHeight()).thenReturn(10);

        layout = spy(new ToggleExpandLayout(context));
        doReturn(2).when(layout).getChildCount();
        doReturn(child0).when(layout).getChildAt(0);
        doReturn(child1).when(layout).getChildAt(1);

        ToggleExpandLayout.OnToggleTouchListener listener = mock(ToggleExpandLayout.OnToggleTouchListener.class);
        layout.setOnToggleTouchListener(listener);

        layout.onLayout(true, 0, 0, 30, 25);
        layout.open();
        layout.close();

        verify(listener, atLeastOnce()).onStartOpen(anyInt(), anyInt());
        verify(listener, atLeastOnce()).onStartClose(anyInt(), anyInt());
    }

    @Test
    public void testMultipleListeners() {
        ToggleExpandLayout.OnToggleTouchListener listener1 = mock(ToggleExpandLayout.OnToggleTouchListener.class);
        ToggleExpandLayout.OnToggleTouchListener listener2 = mock(ToggleExpandLayout.OnToggleTouchListener.class);
        layout.setOnToggleTouchListener(listener1);
        layout.setOnToggleTouchListener(listener2);

        layout.open();
        layout.close();

        verify(listener1, atLeast(0)).onStartOpen(anyInt(), anyInt());
        verify(listener2, atLeast(0)).onStartOpen(anyInt(), anyInt());
    }

}