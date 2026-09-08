package io.github.xiaofeidev.round;

import android.content.Context;
import android.util.AttributeSet;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class RoundFrameLayoutPublicTest {

    @Test
    public void constructor_and_init_minimal_public() {
        Context context = RuntimeEnvironment.getApplication();
        RoundFrameLayout layout = new RoundFrameLayout(context);
        assertNotNull(layout);
        assertTrue(layout instanceof RoundFrameLayout);
        assertNotNull(layout.getRadiusList());
    }

    @Test
    public void constructor_with_attrs_public() {
        Context context = RuntimeEnvironment.getApplication();
        AttributeSet attrs = null;
        RoundFrameLayout layout = new RoundFrameLayout(context, attrs);
        assertNotNull(layout);
        assertNotNull(layout.getRadiusList());
    }

    @Test
    public void testSetAndGetRadius_public() {
        Context context = RuntimeEnvironment.getApplication();
        RoundFrameLayout layout = new RoundFrameLayout(context);
        layout.setRadius(13f);
        assertEquals(13f, layout.getRadius(), 0f);
        layout.setTopRightRadius(8f);
        assertEquals(8f, layout.getTopRightRadius(), 0f);
    }

    @Test
    public void testFillRadiusReflects_public() {
        Context context = RuntimeEnvironment.getApplication();
        RoundFrameLayout layout = new RoundFrameLayout(context);
        layout.setRadius(11f);
        layout.setTopLeftRadius(2.4f);
        layout.setTopRightRadius(4.3f);
        layout.setBottomLeftRadius(6.1f);
        layout.setBottomRightRadius(8.7f);
        layout.fillRadius();
        float[] list = layout.getRadiusList();
        assertEquals(2.4f, list[0], 0.0001f);
        assertEquals(4.3f, list[2], 0.0001f);
        assertEquals(6.1f, list[6], 0.0001f);
        assertEquals(8.7f, list[4], 0.0001f);
    }
}