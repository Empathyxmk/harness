package me.ele.amigo;

import android.support.test.runner.AndroidJUnit4;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(AndroidJUnit4.class)
public class AmigoServicePublicTest {
    @Test
    public void publicTestServiceStarter() {
        // Public variant for service test, different dummy check execution
        Assert.assertEquals(3 * 5, 15);
    }
}