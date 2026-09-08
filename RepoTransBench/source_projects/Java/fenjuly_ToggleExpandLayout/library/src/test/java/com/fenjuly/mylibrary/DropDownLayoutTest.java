package com.fenjuly.mylibrary;

import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
import android.widget.FrameLayout;
import org.junit.Before;
import org.junit.Test;
import static org.mockito.Mockito.*;

/**
 * Unit test for DropDownLayout class.
 */
public class DropDownLayoutTest {

    private DropDownLayout layout;
    private Context context;

    @Before
    public void setUp() {
        context = mock(Context.class);
        layout = spy(new DropDownLayout(context));
    }

    @Test
    public void testOnLayoutWithSimpleChild() {
        // Simulate 1 child not ToggleExpandLayout
        View child = mock(View.class);

        doReturn(1).when(layout).getChildCount();
        doReturn(child).when(layout).getChildAt(0);
        when(child.getMeasuredWidth()).thenReturn(10);
        when(child.getMeasuredHeight()).thenReturn(5);

        layout.onLayout(true, 0, 0, 10, 10);
        // No exception should occur
    }

    @Test
    public void testOnLayoutWithToggleExpandLayoutChild() {
        ToggleExpandLayout toggleChild = mock(ToggleExpandLayout.class);
        View grandChild = mock(View.class);

        doReturn(1).when(layout).getChildCount();
        doReturn(toggleChild).when(layout).getChildAt(0);
        when(toggleChild.getMeasuredWidth()).thenReturn(22);
        when(toggleChild.getMeasuredHeight()).thenReturn(7);
        doReturn(1).when(toggleChild).getChildCount();
        doReturn(grandChild).when(toggleChild).getChildAt(0);
        when(grandChild.getMeasuredWidth()).thenReturn(15);
        when(grandChild.getMeasuredHeight()).thenReturn(3);

        layout.onLayout(false, 1, 2, 3, 4);
        // No exception should occur
    }
}