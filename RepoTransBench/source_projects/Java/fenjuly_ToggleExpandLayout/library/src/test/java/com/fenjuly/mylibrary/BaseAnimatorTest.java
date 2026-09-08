package com.fenjuly.mylibrary;

import android.view.View;
import com.nineoldandroids.animation.Animator;
import com.nineoldandroids.animation.AnimatorSet;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for BaseAnimator class.
 */
public class BaseAnimatorTest {

    private BaseAnimator animator;

    private class TestAnimator extends BaseAnimator {
        boolean prepared = false;
        @Override
        protected void prepare(View target) {
            prepared = true;
        }
    }

    @Before
    public void setUp() {
        animator = new TestAnimator();
    }

    @Test
    public void testDefaultDuration() {
        assertEquals(BaseAnimator.DURATION, animator.getDuration());
    }

    @Test
    public void testSetAnimatorSet() {
        AnimatorSet set = new AnimatorSet();
        animator.setAnimatorSet(set);
        assertEquals(set, animator.getAnimatorSet());
    }

    @Test
    public void testSetGetDuration() {
        animator.setDuration(500);
        assertEquals(500, animator.getDuration());
    }

    @Test
    public void testPrepareAndAnimate() {
        View view = mock(View.class);
        ((TestAnimator) animator).prepared = false;
        animator.animate(view);
        assertTrue(((TestAnimator) animator).prepared);
    }

    @Test
    public void testAddAnimatorListener_andStart() {
        Animator.AnimatorListener listener = mock(Animator.AnimatorListener.class);
        animator.addAnimatorListener(listener);
        animator.start();
        // No exception expected
    }
}