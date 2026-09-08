package com.txusballesteros.widgets;

import android.graphics.RectF;
import org.junit.Test;
import static org.junit.Assert.*;

public class BaseRendererPublicTest {
    static class TestRenderer extends BaseRenderer {
        public TestRenderer(RectF drawingArea, FitChartValue value) {
            super(drawingArea, value);
        }
    }

    @Test
    public void testGetDrawingArea_andGetValue_withDifferentAreaAndValue() {
        RectF area = new RectF(10, 12, 34, 56);
        FitChartValue value = new FitChartValue(55, 0xABCDEF);
        TestRenderer renderer = new TestRenderer(area, value);

        assertSame(area, renderer.getDrawingArea());
        assertSame(value, renderer.getValue());
    }
}