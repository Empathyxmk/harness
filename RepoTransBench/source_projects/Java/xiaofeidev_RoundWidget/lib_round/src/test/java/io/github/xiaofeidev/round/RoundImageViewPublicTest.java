package io.github.xiaofeidev.round;

import android.content.Context;
import android.util.AttributeSet;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class RoundImageViewPublicTest {

    @Test
    public void constructor_and_init_minimal_public() {
        Context context = RuntimeEnvironment.getApplication();
        RoundImageView view = new RoundImageView(context);
        assertNotNull(view);
        assertEquals(RoundImageView.STROKE_MODE_PADDING, 0);
        assertEquals(RoundImageView.STROKE_MODE_OVERLAY, 1);
        assertTrue(view instanceof RoundImageView);
        assertNotNull(view.getRadiusList());
    }

    @Test
    public void constructor_with_attrs_public() {
        Context context = RuntimeEnvironment.getApplication();
        AttributeSet attrs = null;
        RoundImageView view = new RoundImageView(context, attrs);
        assertNotNull(view);
        assertNotNull(view.getRadiusList());
    }

    @Test
    public void testSetAndGetRadius_public() {
        Context context = RuntimeEnvironment.getApplication();
        RoundImageView view = new RoundImageView(context);
        view.setRadius(12f);
        assertEquals(12f, view.getRadius(), 0f);
        view.setTopRightRadius(7f);
        assertEquals(7f, view.getTopRightRadius(), 0f);
    }

    @Test
    public void testFillRadiusReflects_public() {
        Context context = RuntimeEnvironment.getApplication();
        RoundImageView view = new RoundImageView(context);
        view.setRadius(9f);
        view.setTopLeftRadius(2.2f);
        view.setTopRightRadius(3.3f);
        view.setBottomLeftRadius(4.4f);
        view.setBottomRightRadius(5.5f);
        view.fillRadius();
        float[] list = view.getRadiusList();
        assertEquals(2.2f, list[0], 0.0001f);
        assertEquals(3.3f, list[2], 0.0001f);
        assertEquals(4.4f, list[6], 0.0001f);
        assertEquals(5.5f, list[4], 0.0001f);
    }
}