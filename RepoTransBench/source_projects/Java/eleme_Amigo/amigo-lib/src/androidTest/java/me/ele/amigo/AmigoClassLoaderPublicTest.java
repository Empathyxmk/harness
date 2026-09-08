package me.ele.amigo;

import android.support.test.runner.AndroidJUnit4;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(AndroidJUnit4.class)
public class AmigoClassLoaderPublicTest {
    @Test
    public void publicTestClassLoaderSmoke() {
        // Dummy test for public variant, just run different dummy assertion
        Assert.assertFalse("Different dummy assert", false);
    }
}