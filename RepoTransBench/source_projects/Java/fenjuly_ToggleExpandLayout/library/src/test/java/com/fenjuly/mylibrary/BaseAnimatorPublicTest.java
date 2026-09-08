package com.fenjuly.mylibrary;

import android.view.View;
import com.nineoldandroids.animation.AnimatorSet;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

/**
 * Public test for BaseAnimator class using different test data.
 */
public class BaseAnimatorPublicTest {

    private static class DummyAnimator extends BaseAnimator {
        boolean prepared = false;
        @Override
        protected void prepare(View target) {
            prepared = true;
        }
    }

    private DummyAnimator animator;
    private View target;

    @Before
    public void setUp() {
        animator = new DummyAnimator();
        target = mock(View.class);
    }

    @Test
    public void testDurationsAreDifferentPublic() {
        assertEquals(BaseAnimator.DURATION, animator.getDuration());
        animator.setDuration(456);
        assertEquals(456, animator.getDuration());
        animator.setDuration(880);
        assertEquals(880, animator.getDuration());
    }

    @Test
    public void testAnimatorSetPublic() {
        AnimatorSet newSet = new AnimatorSet();
        animator.setAnimatorSet(newSet);
        assertSame(newSet, animator.getAnimatorSet());
    }

    @Test
    public void testAnimatePreparesPublic() {
        assertFalse(animator.prepared);
        animator.animate(target);
        assertTrue(animator.prepared);
    }
}