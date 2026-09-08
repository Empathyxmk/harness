package com.hankkin.library;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.drawable.ColorDrawable;
import android.util.AttributeSet;
import android.widget.ImageView;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class CircleImageViewTest {

    private Context context;

    @Before
    public void setUp() {
        context = RuntimeEnvironment.getApplication();
    }

    @Test
    public void testConstructorsAndInit() {
        CircleImageView civ1 = new CircleImageView(context);
        assertEquals(ImageView.ScaleType.CENTER_CROP, civ1.getScaleType());

        AttributeSet attrs = Mockito.mock(AttributeSet.class);
        CircleImageView civ2 = new CircleImageView(context, attrs);
        assertEquals(ImageView.ScaleType.CENTER_CROP, civ2.getScaleType());
    }

    @Test(expected = IllegalArgumentException.class)
    public void testSetScaleTypeThrows() {
        CircleImageView civ = new CircleImageView(context);
        civ.setScaleType(ImageView.ScaleType.FIT_XY);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testSetAdjustViewBoundsThrows() {
        CircleImageView civ = new CircleImageView(context);
        civ.setAdjustViewBounds(true);
    }

    @Test
    public void testOnDrawWithNoBitmap() {
        CircleImageView civ = new CircleImageView(context);
        Canvas canvas = Mockito.mock(Canvas.class);
        civ.onDraw(canvas); // Should not throw
        // No bitmap set, nothing drawn
    }

    @Test
    public void testSetBorderAndFillColor() {
        CircleImageView civ = new CircleImageView(context);
        civ.setBorderColor(Color.BLUE);
        civ.setBorderWidth(5);
        civ.setFillColor(Color.YELLOW);
        assertEquals(Color.BLUE, civ.getBorderColor());
        assertEquals(5, civ.getBorderWidth());
        assertEquals(Color.YELLOW, civ.getFillColor());
    }

    @Test
    public void testSetDisableCircularTransformation() {
        CircleImageView civ = new CircleImageView(context);
        civ.setDisableCircularTransformation(true);
        assertTrue(civ.isDisableCircularTransformation());
        civ.setDisableCircularTransformation(false);
        assertFalse(civ.isDisableCircularTransformation());
    }
}