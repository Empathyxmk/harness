package com.fenjuly.mylibrary;

import android.content.Context;
import android.util.AttributeSet;
import org.junit.Before;
import org.junit.Test;
import static org.mockito.Mockito.*;

/**
 * Public test for ToggleExpandLayout class using different input.
 * (The real class is likely visual/layout, so these will just check construction/no-op logic.)
 */
public class ToggleExpandLayoutPublicTest {

    private ToggleExpandLayout layout;
    private Context context;
    private AttributeSet attrs;

    @Before
    public void setUp() {
        context = mock(Context.class);
        attrs = mock(AttributeSet.class);
        layout = new ToggleExpandLayout(context, attrs, 123);
    }

    @Test
    public void testConstructorWithDifferentDataPublic() {
        // Test constructor with different defStyleAttr
        ToggleExpandLayout layout2 = new ToggleExpandLayout(context, attrs, 789);
        assertNotNull(layout2);
    }

    @Test
    public void testOpenCloseNoCrash() {
        // Should not throw exceptions
        layout.open();
        layout.close();
    }

    @Test
    public void testSetOnToggleTouchListenerNoCrash() {
        layout.setOnToggleTouchListener(new ToggleExpandLayout.OnToggleTouchListener() {
            @Override public void onStartOpen(int h, int oh) { }
            @Override public void onOpen() { }
            @Override public void onStartClose(int h, int oh) { }
            @Override public void onClosed() { }
        });
        layout.open();
        layout.close();
    }
}