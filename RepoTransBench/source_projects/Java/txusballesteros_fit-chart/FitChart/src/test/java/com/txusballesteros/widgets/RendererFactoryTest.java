package com.txusballesteros.widgets;

import android.graphics.RectF;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class RendererFactoryTest {
    @Test
    public void testReturnsLinearRenderer() {
        FitChartValue value = mock(FitChartValue.class);
        RectF rect = new RectF(0,0,100,100);
        Renderer renderer = RendererFactory.getRenderer(AnimationMode.LINEAR, value, rect);
        assertTrue(renderer instanceof LinearValueRenderer);
    }

    @Test
    public void testReturnsOverdrawRenderer() {
        FitChartValue value = mock(FitChartValue.class);
        RectF rect = new RectF(0,0,100,100);
        Renderer renderer = RendererFactory.getRenderer(AnimationMode.OVERDRAW, value, rect);
        assertTrue(renderer instanceof OverdrawValueRenderer);
    }
}