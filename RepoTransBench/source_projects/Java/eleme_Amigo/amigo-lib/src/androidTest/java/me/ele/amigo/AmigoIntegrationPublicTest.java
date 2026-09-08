package me.ele.amigo;

import android.support.test.runner.AndroidJUnit4;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(AndroidJUnit4.class)
public class AmigoIntegrationPublicTest {
    @Test
    public void publicTestIntegrationSmoke() {
        // Pure smoke assertion for instrumentation, with changed values
        Assert.assertNotSame("Not equal values", 100, 200);
    }
}