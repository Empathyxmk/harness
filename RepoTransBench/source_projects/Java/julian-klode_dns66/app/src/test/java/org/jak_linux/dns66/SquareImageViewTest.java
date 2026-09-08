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
public class SquareImageViewTest {

    private Context context;

    @Before
    public void setUp() {
        context = ApplicationProvider.getApplicationContext();
    }

    @Test
    @Config(sdk = 19)
    public void testConstructorAndOnMeasureSdk19() {
        SquareImageView view = new SquareImageView(context);
        view.measure(100, 200);
        int w = view.getMeasuredWidth();
        int h = view.getMeasuredHeight();
        Assert.assertEquals(w, h); // should be square
    }

    @Test
    @Config(sdk = 23)
    public void testConstructorAndOnMeasureSdk23() {
        SquareImageView view = new SquareImageView(context);
        view.measure(110, 50);
        int w = view.getMeasuredWidth();
        int h = view.getMeasuredHeight();
        Assert.assertEquals(110, w);
        Assert.assertEquals(50, h);
    }
}