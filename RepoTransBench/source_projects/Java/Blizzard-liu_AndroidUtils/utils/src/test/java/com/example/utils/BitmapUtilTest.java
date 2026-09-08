package com.example.utils;

import android.graphics.BitmapFactory;
import org.junit.Test;

import static org.junit.Assert.*;

public class BitmapUtilTest {

    @Test
    public void testCalculateInSampleSize_largeImage() {
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.outWidth = 900;
        options.outHeight = 900;
        BitmapFactory.Options out = BitmapUtil.calculateInSampleSize(options, 450, 400);
        assertEquals(options, out);
        assertEquals(false, out.inJustDecodeBounds);
        assertTrue(out.inSampleSize > 1);
    }

    @Test
    public void testCalculateInSampleSize_smallImage() {
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.outWidth = 200;
        options.outHeight = 100;
        BitmapFactory.Options out = BitmapUtil.calculateInSampleSize(options, 450, 400);
        assertEquals(options, out);
        assertEquals(false, out.inJustDecodeBounds);
        assertEquals(1, out.inSampleSize);
    }

    @Test(expected = Error.class)
    public void testConstructor_throwsError() {
        new BitmapUtil();
    }
}