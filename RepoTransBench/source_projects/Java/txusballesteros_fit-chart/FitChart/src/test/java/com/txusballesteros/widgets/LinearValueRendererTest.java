package com.txusballesteros.widgets;

import android.graphics.RectF;
import android.graphics.Path;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class LinearValueRendererTest {
    @Test
    public void testBuildPath_withStartAngleLessThanSeek_buildsArc() {
        RectF area = new RectF(0, 0, 100, 100);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(0f);
        when(value.getSweepAngle()).thenReturn(100f);
        LinearValueRenderer renderer = new LinearValueRenderer(area, value);

        Path path = renderer.buildPath(0.5f, 50f);

        assertNotNull(path);
    }

    @Test
    public void testBuildPath_withStartAngleGreaterThanSeek_returnsNull() {
        RectF area = new RectF(0, 0, 100, 100);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(100f);
        when(value.getSweepAngle()).thenReturn(50f);
        LinearValueRenderer renderer = new LinearValueRenderer(area, value);

        Path path = renderer.buildPath(0.5f, 40f);

        assertNull(path);
    }

    @Test
    public void testCalculateSweepAngle_pathBranches() {
        RectF area = new RectF(0, 0, 100, 100);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(20f);
        when(value.getSweepAngle()).thenReturn(50f);
        LinearValueRenderer renderer = new LinearValueRenderer(area, value);

        // force totalSizeOfValue > animationSeek
        renderer.buildPath(0.5f, 40f);
        // force totalSizeOfValue <= animationSeek
        renderer.buildPath(0.5f, 80f);
    }
}