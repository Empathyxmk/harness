package com.txusballesteros.widgets;

import android.graphics.RectF;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class BaseRendererTest {
    static class ConcreteRenderer extends BaseRenderer {
        public ConcreteRenderer(RectF drawingArea, FitChartValue value) {
            super(drawingArea, value);
        }
    }

    @Test
    public void testGetters() {
        RectF area = new RectF(1,2,3,4);
        FitChartValue val = mock(FitChartValue.class);
        BaseRenderer renderer = new ConcreteRenderer(area, val);

        assertEquals(area, renderer.getDrawingArea());
        assertEquals(val, renderer.getValue());
    }
}