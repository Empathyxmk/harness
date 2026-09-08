package com.shadev.easyloadingdemo.view;

import android.content.Context;
import android.graphics.drawable.Drawable;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class LoadingButtonPublicTest {

    private LoadingButton loadingButton;

    @Before
    public void setUp() {
        Context context = RuntimeEnvironment.getApplication();
        loadingButton = new LoadingButton(context, null, 0) {
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
    public void testInitialState_publicVariant() {
        assertFalse(loadingButton.isCompleted());
        assertFalse(loadingButton.isShowArc());
    }

    @Test
    public void testSetTargetProgress_setsDifferentProgress() {
        loadingButton.setTargetProgress(250); // different from 180 in original
        assertEquals(250, loadingButton.getTargetProgress());
    }

    @Test
    public void testSetAndGetCallback_public() {
        final boolean[] flag = new boolean[1];
        LoadingButton.Callback cb = new LoadingButton.Callback() {
            @Override
            public void complete() {
                flag[0] = true;
            }
        };
        loadingButton.setCallback(cb);
        loadingButton.performCompleteCallback();
        assertTrue(flag[0]);
    }

    @Test
    public void testSetCompleted_alternatePattern() {
        loadingButton.setCompleted(false);
        assertFalse(loadingButton.isCompleted());
        loadingButton.setCompleted(true);
        assertTrue(loadingButton.isCompleted());
    }

    @Test
    public void testOnClick_withCompleted_Public() {
        loadingButton.setCompleted(true);
        assertTrue(loadingButton.isCompleted());
        loadingButton.performClick();
        // Nothing to assert, just to cover
    }

    @Test
    public void testOnClick_withNotCompleted_Public() {
        loadingButton.setCompleted(false);
        loadingButton.performClick(); // should not throw
        // Nothing to assert, just to cover
    }

    @Test
    public void testSetShowArc_public() {
        loadingButton.setShowArc(false);
        assertFalse(loadingButton.isShowArc());
        loadingButton.setShowArc(true);
        assertTrue(loadingButton.isShowArc());
    }
}