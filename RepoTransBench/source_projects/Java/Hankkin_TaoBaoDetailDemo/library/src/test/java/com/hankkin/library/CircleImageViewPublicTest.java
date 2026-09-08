package com.hankkin.library;

import android.content.Context;
import android.graphics.Color;
import android.util.AttributeSet;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public tests for CircleImageView using different test data.
 */
public class CircleImageViewPublicTest {

    // Simple mock Context
    public static class MockContext extends android.test.mock.MockContext {}

    @Test
    public void testBorderColorChange() {
        Context context = new MockContext();
        CircleImageView civ = new CircleImageView(context);
        civ.setBorderColor(Color.RED);
        assertEquals(Color.RED, civ.getBorderColor());

        civ.setBorderColor(Color.GREEN);
        assertEquals(Color.GREEN, civ.getBorderColor());
    }

    @Test
    public void testBorderWidthChange() {
        Context context = new MockContext();
        CircleImageView civ = new CircleImageView(context);
        civ.setBorderWidth(8);
        assertEquals(8, civ.getBorderWidth());

        civ.setBorderWidth(0);
        assertEquals(0, civ.getBorderWidth());
    }

    @Test
    public void testFillColorChange() {
        Context context = new MockContext();
        CircleImageView civ = new CircleImageView(context);
        civ.setFillColor(Color.YELLOW);
        assertEquals(Color.YELLOW, civ.getFillColor());

        civ.setFillColor(Color.CYAN);
        assertEquals(Color.CYAN, civ.getFillColor());
    }

    @Test
    public void testBorderOverlayChange() {
        Context context = new MockContext();
        CircleImageView civ = new CircleImageView(context);
        civ.setBorderOverlay(true);
        assertTrue(civ.isBorderOverlay());

        civ.setBorderOverlay(false);
        assertFalse(civ.isBorderOverlay());
    }
}