package com.fenjuly.mylibrary;

import android.content.Context;
import android.view.View;
import org.junit.Before;
import org.junit.Test;
import static org.mockito.Mockito.*;

/**
 * Public test for DropDownLayout class.
 * Uses different input/output test data from DropDownLayoutTest.
 */
public class DropDownLayoutPublicTest {

    private DropDownLayout layout;
    private Context context;

    @Before
    public void setUp() {
        context = mock(Context.class);
        layout = spy(new DropDownLayout(context));
    }

    @Test
    public void testOnLayoutWithDifferentSimpleChild() {
        // Simulate 2 children, both not ToggleExpandLayout
        View child1 = mock(View.class);
        View child2 = mock(View.class);

        doReturn(2).when(layout).getChildCount();
        doReturn(child1).when(layout).getChildAt(0);
        doReturn(child2).when(layout).getChildAt(1);
        when(child1.getMeasuredWidth()).thenReturn(13);
        when(child1.getMeasuredHeight()).thenReturn(8);
        when(child2.getMeasuredWidth()).thenReturn(17);
        when(child2.getMeasuredHeight()).thenReturn(4);

        layout.onLayout(true, 2, 3, 7, 12);
        // No exception should occur
    }

    @Test
    public void testOnLayoutWithDifferentToggleExpandLayoutChild() {
        // Simulate 2 children, first is ToggleExpandLayout
        ToggleExpandLayout toggleChild = mock(ToggleExpandLayout.class);
        View grandChild1 = mock(View.class);
        View grandChild2 = mock(View.class);

        View child2 = mock(View.class);

        doReturn(2).when(layout).getChildCount();
        doReturn(toggleChild).when(layout).getChildAt(0);
        doReturn(child2).when(layout).getChildAt(1);

        when(toggleChild.getMeasuredWidth()).thenReturn(30);
        when(toggleChild.getMeasuredHeight()).thenReturn(6);
        doReturn(2).when(toggleChild).getChildCount();
        doReturn(grandChild1).when(toggleChild).getChildAt(0);
        doReturn(grandChild2).when(toggleChild).getChildAt(1);
        when(grandChild1.getMeasuredWidth()).thenReturn(20);
        when(grandChild1.getMeasuredHeight()).thenReturn(5);
        when(grandChild2.getMeasuredWidth()).thenReturn(9);
        when(grandChild2.getMeasuredHeight()).thenReturn(2);

        when(child2.getMeasuredWidth()).thenReturn(14);
        when(child2.getMeasuredHeight()).thenReturn(7);

        layout.onLayout(false, 4, 5, 6, 10);
        // No exception should occur
    }
}