package com.txusballesteros.widgets;

import android.graphics.RectF;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class RendererFactoryPublicTest {
    @Test
    public void testCreateRenderer_returnsLinearValueRendererWithDifferentArea() {
        FitChartValue value = mock(FitChartValue.class);
        RectF area = new RectF(1, 2, 80, 60);

        Renderer renderer = RendererFactory.create(area, value, AnimationMode.LINEAR);

        assertTrue(renderer instanceof LinearValueRenderer);
    }

    @Test
    public void testCreateRenderer_returnsOverdrawValueRendererWithDifferentArea() {
        FitChartValue value = mock(FitChartValue.class);
        RectF area = new RectF(3, 4, 70, 30);

        Renderer renderer = RendererFactory.create(area, value, AnimationMode.OVERDRAW);

        assertTrue(renderer instanceof OverdrawValueRenderer);
    }
}