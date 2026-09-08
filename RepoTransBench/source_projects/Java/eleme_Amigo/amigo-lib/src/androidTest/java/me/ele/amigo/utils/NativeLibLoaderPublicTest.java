package me.ele.amigo.utils;

import android.support.test.runner.AndroidJUnit4;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(AndroidJUnit4.class)
public class NativeLibLoaderPublicTest {
    @Test
    public void publicTestNativeLoaderPub() {
        Assert.assertTrue("Public dummy native", 6 > 2);
    }
}