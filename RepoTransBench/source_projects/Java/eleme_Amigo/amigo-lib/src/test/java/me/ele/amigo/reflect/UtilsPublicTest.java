package me.ele.amigo.reflect;

import org.junit.Assert;
import org.junit.Test;

public class UtilsPublicTest {

    @Test
    public void publicTestIsSameLengthDiff() {
        Integer[] shortArray = new Integer[4];
        Integer[] longArray = new Integer[12];
        Object[] objects = new Object[4];

        Assert.assertFalse(Utils.isSameLength(shortArray, longArray));
        Assert.assertFalse(Utils.isSameLength(longArray, shortArray));
        Assert.assertFalse(Utils.isSameLength(null, shortArray));
        Assert.assertFalse(Utils.isSameLength(shortArray, null));
        Assert.assertTrue(Utils.isSameLength(shortArray, objects));
        Assert.assertTrue(Utils.isSameLength(objects, shortArray));
    }

    @Test
    public void publicTestToClassDiff() {
        Assert.assertEquals(String.class, Utils.toClass("Hello")[0]);
        Assert.assertNotEquals(String.class, Utils.toClass(42)[0]);
        Assert.assertNotEquals(new Class[] {Double.class, String.class},
                Utils.toClass(9.4, "hey"));
    }
}