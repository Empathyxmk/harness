package com.txusballesteros.widgets;

import android.graphics.RectF;
import android.graphics.Path;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class OverdrawValueRendererTest {
    @Test
    public void testBuildPath() {
        RectF area = new RectF(0,0,100,100);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(10f);
        when(value.getSweepAngle()).thenReturn(100f);
        OverdrawValueRenderer renderer = new OverdrawValueRenderer(area, value);

        Path path = renderer.buildPath(0.5f, 50f);

        assertNotNull(path);
    }
}