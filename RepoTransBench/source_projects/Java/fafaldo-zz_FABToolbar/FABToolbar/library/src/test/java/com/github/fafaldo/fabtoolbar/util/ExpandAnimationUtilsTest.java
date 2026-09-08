package com.github.fafaldo.fabtoolbar.util;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import android.animation.Animator;
import android.view.View;
import android.view.ViewGroup;

import org.junit.Before;
import org.junit.Test;

import java.util.List;

public class ExpandAnimationUtilsTest {

    private ViewGroup mockViewGroup;
    private View mockChild1;
    private View mockChild2;

    @Before
    public void setup() {
        mockViewGroup = mock(ViewGroup.class);
        mockChild1 = mock(View.class);
        mockChild2 = mock(View.class);

        when(mockViewGroup.getChildCount()).thenReturn(2);
        when(mockViewGroup.getChildAt(0)).thenReturn(mockChild1);
        when(mockViewGroup.getChildAt(1)).thenReturn(mockChild2);

        // Set up position/size for children
        when(mockChild1.getLeft()).thenReturn(10);
        when(mockChild1.getTop()).thenReturn(20);
        when(mockChild1.getWidth()).thenReturn(30);
        when(mockChild1.getHeight()).thenReturn(40);

        when(mockChild2.getLeft()).thenReturn(100);
        when(mockChild2.getTop()).thenReturn(200);
        when(mockChild2.getWidth()).thenReturn(50);
        when(mockChild2.getHeight()).thenReturn(60);
    }

    @Test
    public void testBuild() {
        int pivotX = 50;
        int pivotY = 60;
        float fraction = 0.5f;
        int duration = 300;
        int delay = 50;

        List<Animator> animators = ExpandAnimationUtils.build(mockViewGroup, pivotX, pivotY, fraction, duration, delay);

        // Should be 2 children x2 (x,y) = 4 anims, plus 1 alpha = 5
        assertEquals(5, animators.size());
        for (int i = 0; i < 4; i++) {
            Animator a = animators.get(i);
            assertNotNull(a);
        }
        // Alpha animator also present
        assertNotNull(animators.get(4));
    }

    @Test
    public void testBuildReversed() {
        int pivotX = 30;
        int pivotY = 90;
        float fraction = 0.3f;
        int duration = 400;
        int delay = 20;

        List<Animator> animators = ExpandAnimationUtils.buildReversed(mockViewGroup, pivotX, pivotY, fraction, duration, delay);

        // 2 children x2 + 1 alpha
        assertEquals(5, animators.size());
        for (int i = 0; i < 5; i++) {
            assertNotNull(animators.get(i));
        }
    }
}