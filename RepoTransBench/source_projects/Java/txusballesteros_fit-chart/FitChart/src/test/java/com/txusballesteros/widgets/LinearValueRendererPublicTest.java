package com.txusballesteros.widgets;

import android.graphics.RectF;
import android.graphics.Path;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class LinearValueRendererPublicTest {
    @Test
    public void testBuildPath_withDifferentStartAngleLessThanSeek_buildsArc() {
        RectF area = new RectF(5, 5, 120, 120);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(10f);
        when(value.getSweepAngle()).thenReturn(30f);
        LinearValueRenderer renderer = new LinearValueRenderer(area, value);

        Path path = renderer.buildPath(0.7f, 25f);

        assertNotNull(path);
    }

    @Test
    public void testBuildPath_withDifferentStartAngleGreaterThanSeek_returnsNull() {
        RectF area = new RectF(10, 10, 80, 80);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(60f);
        when(value.getSweepAngle()).thenReturn(15f);
        LinearValueRenderer renderer = new LinearValueRenderer(area, value);

        Path path = renderer.buildPath(0.3f, 40f);

        assertNull(path);
    }

    @Test
    public void testCalculateSweepAngle_branchesWithDifferentData() {
        RectF area = new RectF(5, 5, 90, 90);
        FitChartValue value = mock(FitChartValue.class);
        when(value.getStartAngle()).thenReturn(5f);
        when(value.getSweepAngle()).thenReturn(25f);
        LinearValueRenderer renderer = new LinearValueRenderer(area, value);

        // force totalSizeOfValue > animationSeek
        renderer.buildPath(0.3f, 20f);
        // force totalSizeOfValue <= animationSeek
        renderer.buildPath(0.6f, 40f);
    }
}