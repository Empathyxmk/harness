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
public class RoundFrameLayoutTest {

    @Test
    public void constructor_and_init_minimal() {
        Context context = RuntimeEnvironment.getApplication();
        RoundFrameLayout layout = new RoundFrameLayout(context);
        assertNotNull(layout);
        assertTrue(layout instanceof RoundFrameLayout);
        assertNotNull(layout.getRadiusList());
    }

    @Test
    public void constructor_with_attrs() {
        Context context = RuntimeEnvironment.getApplication();
        // Manually create attributes compatible with attribute set, but Robolectric can't really fetch custom attrs
        AttributeSet attrs = null;
        RoundFrameLayout layout = new RoundFrameLayout(context, attrs);
        assertNotNull(layout);
        assertNotNull(layout.getRadiusList());
    }

    @Test
    public void testSetAndGetRadius() {
        Context context = RuntimeEnvironment.getApplication();
        RoundFrameLayout layout = new RoundFrameLayout(context);
        layout.setRadius(5f);
        assertEquals(5f, layout.getRadius(), 0f);
        layout.setTopRightRadius(2f);
        assertEquals(2f, layout.getTopRightRadius(), 0f);
    }

    @Test
    public void testFillRadiusReflects() {
        Context context = RuntimeEnvironment.getApplication();
        RoundFrameLayout layout = new RoundFrameLayout(context);
        layout.setRadius(7f);
        layout.setTopLeftRadius(1.2f);
        layout.setTopRightRadius(2.3f);
        layout.setBottomLeftRadius(3.4f);
        layout.setBottomRightRadius(4.5f);
        layout.fillRadius();
        float[] list = layout.getRadiusList();
        assertEquals(1.2f, list[0], 0.0001f);
        assertEquals(2.3f, list[2], 0.0001f);
        assertEquals(3.4f, list[6], 0.0001f);
        assertEquals(4.5f, list[4], 0.0001f);
    }
}