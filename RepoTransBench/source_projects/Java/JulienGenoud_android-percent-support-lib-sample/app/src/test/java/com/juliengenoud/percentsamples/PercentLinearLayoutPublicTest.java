package com.juliengenoud.percentsamples;

import android.content.Context;
import android.util.AttributeSet;
import android.widget.LinearLayout;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class PercentLinearLayoutPublicTest {

    private PercentLinearLayout percentLinearLayout;

    @Before
    public void setUp() {
        Context mockContext = Mockito.mock(Context.class);
        AttributeSet mockAttrs = Mockito.mock(AttributeSet.class);
        percentLinearLayout = new PercentLinearLayout(mockContext, mockAttrs);
    }

    @Test
    public void testGenerateLayoutParamsPublic() {
        AttributeSet anotherMockAttrs = Mockito.mock(AttributeSet.class);
        PercentLinearLayout.LayoutParams params = percentLinearLayout.generateLayoutParams(anotherMockAttrs);
        assertNotNull(params);
        assertTrue(params instanceof PercentLinearLayout.LayoutParams);
    }

    @Test
    public void testLayoutParamsConstructorsPublic() {
        // Use different width/height values from the original test
        LinearLayout.LayoutParams baseParams = new LinearLayout.LayoutParams(50, 75);
        PercentLinearLayout.LayoutParams copy1 = new PercentLinearLayout.LayoutParams(baseParams);
        assertEquals(50, copy1.width);
        assertEquals(75, copy1.height);

        PercentLinearLayout.LayoutParams copy2 = new PercentLinearLayout.LayoutParams(200, 125);
        assertEquals(200, copy2.width);
        assertEquals(125, copy2.height);

        LinearLayout.MarginLayoutParams marginParams = new LinearLayout.MarginLayoutParams(8, 14);
        PercentLinearLayout.LayoutParams copy3 = new PercentLinearLayout.LayoutParams(marginParams);
        assertEquals(8, copy3.width);
        assertEquals(14, copy3.height);
    }
}