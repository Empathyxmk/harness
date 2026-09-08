package com.juliengenoud.percentsamples;

import android.content.Context;
import android.util.AttributeSet;
import android.widget.LinearLayout;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class PercentLinearLayoutTest {

    private PercentLinearLayout percentLinearLayout;

    @Before
    public void setUp() {
        Context mockContext = Mockito.mock(Context.class);
        AttributeSet mockAttrs = Mockito.mock(AttributeSet.class);
        percentLinearLayout = new PercentLinearLayout(mockContext, mockAttrs);
    }

    @Test
    public void testGenerateLayoutParams() {
        AttributeSet mockAttrs = Mockito.mock(AttributeSet.class);
        PercentLinearLayout.LayoutParams params = percentLinearLayout.generateLayoutParams(mockAttrs);
        assertNotNull(params);
        assertTrue(params instanceof PercentLinearLayout.LayoutParams);
    }

    @Test
    public void testLayoutParamsConstructors() {
        LinearLayout.LayoutParams baseParams = new LinearLayout.LayoutParams(123, 456);
        PercentLinearLayout.LayoutParams copy1 = new PercentLinearLayout.LayoutParams(baseParams);
        assertEquals(123, copy1.width);
        assertEquals(456, copy1.height);

        PercentLinearLayout.LayoutParams copy2 = new PercentLinearLayout.LayoutParams(321, 654);
        assertEquals(321, copy2.width);
        assertEquals(654, copy2.height);

        LinearLayout.MarginLayoutParams marginParams = new LinearLayout.MarginLayoutParams(7, 8);
        PercentLinearLayout.LayoutParams copy3 = new PercentLinearLayout.LayoutParams(marginParams);
        assertEquals(7, copy3.width);
        assertEquals(8, copy3.height);
    }
}