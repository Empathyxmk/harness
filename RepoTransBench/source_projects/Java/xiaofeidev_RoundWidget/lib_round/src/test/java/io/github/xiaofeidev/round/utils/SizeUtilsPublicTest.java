package io.github.xiaofeidev.round.utils;

import android.content.Context;
import android.content.res.Resources;
import android.util.DisplayMetrics;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import static org.junit.Assert.*;

@RunWith(RobolectricTestRunner.class)
public class SizeUtilsPublicTest {

    @Test
    public void testDp2PxAndPx2Dp_public() {
        Context context = RuntimeEnvironment.getApplication();
        Resources resources = context.getResources();
        DisplayMetrics metrics = resources.getDisplayMetrics();

        float density = metrics.density;
        int px = SizeUtils.dp2px(context, 15f);
        float expectedPx = 15f * density;
        assertEquals((int) (expectedPx + 0.5f), px);

        float dp = SizeUtils.px2dp(context, px);
        assertEquals(15f, dp, 0.5f);
    }

    @Test
    public void testSp2PxAndPx2Sp_public() {
        Context context = RuntimeEnvironment.getApplication();
        Resources resources = context.getResources();
        DisplayMetrics metrics = resources.getDisplayMetrics();

        float scaledDensity = metrics.scaledDensity;
        int px = SizeUtils.sp2px(context, 10f);
        float expectedPx = 10f * scaledDensity;
        assertEquals((int) (expectedPx + 0.5f), px);

        float sp = SizeUtils.px2sp(context, px);
        assertEquals(10f, sp, 0.5f);
    }
}