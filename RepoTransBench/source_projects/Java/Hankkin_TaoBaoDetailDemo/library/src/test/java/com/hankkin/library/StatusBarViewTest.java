package com.hankkin.library;

import android.content.Context;
import android.util.AttributeSet;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class StatusBarViewTest {

    @Test
    public void testConstructors() {
        Context context = RuntimeEnvironment.getApplication();
        StatusBarView sbv1 = new StatusBarView(context);
        assertNotNull(sbv1);

        AttributeSet attrs = Mockito.mock(AttributeSet.class);
        StatusBarView sbv2 = new StatusBarView(context, attrs);
        assertNotNull(sbv2);
    }
}