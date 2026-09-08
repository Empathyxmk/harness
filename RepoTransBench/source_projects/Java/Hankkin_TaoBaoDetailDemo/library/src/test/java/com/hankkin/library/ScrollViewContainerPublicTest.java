package com.hankkin.library;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;
import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Public test for ScrollViewContainer with different test event scenario.
 */
public class ScrollViewContainerPublicTest {

    public static class MyMockContext extends android.test.mock.MockContext {}

    @Test
    public void testConstructor() {
        Context ctx = new MyMockContext();
        ScrollViewContainer svc1 = new ScrollViewContainer(ctx);
        assertNotNull(svc1);

        AttributeSet attrs = null;
        ScrollViewContainer svc2 = new ScrollViewContainer(ctx, attrs);
        assertNotNull(svc2);
    }

    @Test
    public void testTouchEventDispatchReturnsTrueOnACTION_UP() {
        Context ctx = new MyMockContext();
        ScrollViewContainer svc = new ScrollViewContainer(ctx);
        MotionEvent upEvent = MotionEvent.obtain(100, 200, MotionEvent.ACTION_UP, 12.0f, 24.0f, 0);
        boolean result = svc.dispatchTouchEvent(upEvent);
        // Should always return true
        assertTrue(result);
        upEvent.recycle();
    }
}