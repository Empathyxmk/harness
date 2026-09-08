package com.shadev.easyloadingdemo.view;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.os.Build;
import android.util.AttributeSet;
import android.view.View;
import android.view.animation.Animation;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class LoadingButtonTest {

    private LoadingButton loadingButton;

    @Before
    public void setUp() {
        Context context = RuntimeEnvironment.getApplication();
        loadingButton = new LoadingButton(context, null, 0) {
            // Mock resource drawables to avoid NPE.
            @Override
            protected Drawable getDrawable(int id) {
                return new Drawable() {
                    @Override
                    public void draw(android.graphics.Canvas canvas) {}
                    @Override
                    public void setAlpha(int alpha) {}
                    @Override
                    public void setColorFilter(android.graphics.ColorFilter colorFilter) {}
                    @Override
                    public int getOpacity() { return android.graphics.PixelFormat.OPAQUE; }
                };
            }
        };
    }

    @Test
    public void testInitialState() {
        assertFalse(loadingButton.isCompleted());
        assertFalse(loadingButton.isShowArc());
    }

    @Test
    public void testSetTargetProgress_setsProgress() {
        loadingButton.setTargetProgress(180);
        assertEquals(180, loadingButton.getTargetProgress());
    }

    @Test
    public void testSetAndGetCallback() {
        final boolean[] wasCalled = new boolean[1];
        LoadingButton.Callback callback = () -> wasCalled[0] = true;
        loadingButton.setCallback(callback);
        loadingButton.performCompleteCallback();
        assertTrue(wasCalled[0]);
    }

    @Test
    public void testSetCompleted() {
        loadingButton.setCompleted(true);
        assertTrue(loadingButton.isCompleted());
        loadingButton.setCompleted(false);
        assertFalse(loadingButton.isCompleted());
    }

    @Test
    public void testOnClick_withNotCompleted() {
        // Simulate not completed, should trigger animation (handler covered).
        loadingButton.setCompleted(false);
        loadingButton.performClick(); // Animation flow can't check visually, but should not throw
    }

    @Test
    public void testOnClick_withCompleted() {
        loadingButton.setCompleted(true);
        assertTrue(loadingButton.isCompleted());
        // Should return immediately, animation won't occur
        loadingButton.performClick();
    }

    // Additional branch: setShowArc
    @Test
    public void testSetShowArc() {
        loadingButton.setShowArc(true);
        assertTrue(loadingButton.isShowArc());
        loadingButton.setShowArc(false);
        assertFalse(loadingButton.isShowArc());
    }
}