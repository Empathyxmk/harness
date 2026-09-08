package io.github.xiaofeidev.round;

import android.content.Context;
import android.os.Build;
import android.util.AttributeSet;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class RoundImageViewTest {

    @Test
    public void constructor_and_init_minimal() {
        Context context = RuntimeEnvironment.getApplication();
        RoundImageView view = new RoundImageView(context);
        assertNotNull(view);
        assertTrue(view instanceof RoundImageView);
        assertNotNull(view.getRadiusList());
        assertEquals(RoundImageView.STROKE_MODE_PADDING, 0);
        assertEquals(RoundImageView.STROKE_MODE_OVERLAY, 1);
    }

    @Test
    public void constructor_with_attrs() {
        Context context = RuntimeEnvironment.getApplication();
        AttributeSet attrs = null;
        RoundImageView view = new RoundImageView(context, attrs);
        assertNotNull(view);
        assertNotNull(view.getRadiusList());
    }

    @Test
    public void testSetAndGetRadius() {
        Context context = RuntimeEnvironment.getApplication();
        RoundImageView view = new RoundImageView(context);
        view.setRadius(6f);
        assertEquals(6f, view.getRadius(), 0f);
        view.setTopRightRadius(4f);
        assertEquals(4f, view.getTopRightRadius(), 0f);
    }

    @Test
    public void testFillRadiusReflects() {
        Context context = RuntimeEnvironment.getApplication();
        RoundImageView view = new RoundImageView(context);
        view.setRadius(8f);
        view.setTopLeftRadius(1.1f);
        view.setTopRightRadius(2.2f);
        view.setBottomLeftRadius(3.3f);
        view.setBottomRightRadius(4.4f);
        view.fillRadius();
        float[] list = view.getRadiusList();
        assertEquals(1.1f, list[0], 0.0001f);
        assertEquals(2.2f, list[2], 0.0001f);
        assertEquals(3.3f, list[6], 0.0001f);
        assertEquals(4.4f, list[4], 0.0001f);
    }
}