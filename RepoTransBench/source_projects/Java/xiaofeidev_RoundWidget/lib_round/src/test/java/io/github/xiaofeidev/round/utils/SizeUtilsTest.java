package io.github.xiaofeidev.round.utils;

import org.junit.Test;
import static org.junit.Assert.*;

public class SizeUtilsTest {

    @Test
    public void testDp2PxAndPx2DpConsistency() {
        float dp = 10f;
        float px = SizeUtils.dp2px(dp);
        float dpResult = SizeUtils.px2dp(px);

        // dpResult should be close to original dp value
        assertEquals(dp, dpResult, 0.5f);
    }

    @Test
    public void testZero() {
        assertEquals(0f, SizeUtils.dp2px(0f), 0.0001f);
        assertEquals(0, SizeUtils.px2dp(0f));
    }

    @Test
    public void testDp2PxKnownValue() {
        float density = android.content.res.Resources.getSystem().getDisplayMetrics().density;
        assertEquals(20f * density, SizeUtils.dp2px(20f), 0.0001f);
    }

    @Test
    public void testPx2DpKnownValue() {
        float density = android.content.res.Resources.getSystem().getDisplayMetrics().density;
        float px = 50f;
        int expectedDp = (int)(px / density + 0.5f);
        assertEquals(expectedDp, SizeUtils.px2dp(px));
    }
}