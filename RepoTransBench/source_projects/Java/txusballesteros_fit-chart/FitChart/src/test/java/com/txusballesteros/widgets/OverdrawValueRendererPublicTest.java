package com.txusballesteros.widgets;

import android.graphics.RectF;
import android.graphics.Path;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class OverdrawValueRendererPublicTest {
    @Test
    public void testBuildPath_withOtherAngles() {
        RectF area = new RectF(2, 2, 50, 50);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(30f);
        when(value.getSweepAngle()).thenReturn(45f);
        OverdrawValueRenderer renderer = new OverdrawValueRenderer(area, value);

        Path path = renderer.buildPath(0.6f, 35f);

        assertNotNull(path);
    }
}