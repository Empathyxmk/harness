package com.hankkin.library;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.widget.RelativeLayout;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class ScrollViewContainerTest {

    private Context context;

    @Before
    public void setUp() {
        context = RuntimeEnvironment.getApplication();
    }

    @Test
    public void testConstructorsAndInit() {
        ScrollViewContainer sc1 = new ScrollViewContainer(context);
        assertNotNull(sc1);
        AttributeSet attrs = null;
        ScrollViewContainer sc2 = new ScrollViewContainer(context, attrs);
        assertNotNull(sc2);
        ScrollViewContainer sc3 = new ScrollViewContainer(context, attrs, 0);
        assertNotNull(sc3);
    }
}