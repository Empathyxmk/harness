package org.jak_linux.dns66;

import android.content.Context;
import android.os.Build;
import android.util.AttributeSet;
import androidx.test.core.app.ApplicationProvider;
import org.junit.*;
import org.junit.runner.RunWith;
import org.robolectric.*;
import org.robolectric.annotation.Config;

@RunWith(RobolectricTestRunner.class)
public class SquareImageViewPublicTest {

    private Context context;

    @Before
    public void setUp() {
        context = ApplicationProvider.getApplicationContext();
    }

    @Test
    @Config(sdk = 18)
    public void testConstructorAndOnMeasureSdk18() {
        SquareImageView view = new SquareImageView(context);
        view.measure(120, 180);
        int w = view.getMeasuredWidth();
        int h = view.getMeasuredHeight();
        Assert.assertEquals(w, h); // should be square
    }

    @Test
    @Config(sdk = 21)
    public void testConstructorAndOnMeasureSdk21() {
        SquareImageView view = new SquareImageView(context);
        view.measure(60, 90);
        int w = view.getMeasuredWidth();
        int h = view.getMeasuredHeight();
        Assert.assertEquals(60, w);
        Assert.assertEquals(90, h);
    }
}