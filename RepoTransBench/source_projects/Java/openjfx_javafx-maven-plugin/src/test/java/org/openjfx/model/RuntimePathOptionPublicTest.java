package org.openjfx.model;

import org.junit.Assert;
import org.junit.Test;

public class RuntimePathOptionPublicTest {

    @Test
    public void testValueOfDifferentData() {
        Assert.assertEquals(RuntimePathOption.MODULEPATH, RuntimePathOption.valueOf("MODULEPATH"));
        Assert.assertEquals(RuntimePathOption.CLASSPATH, RuntimePathOption.valueOf("CLASSPATH"));
    }

    @Test
    public void testValuesArrayLengthAndContentDifferentOrder() {
        RuntimePathOption[] values = RuntimePathOption.values();
        Assert.assertTrue(values.length >= 2);
        Assert.assertTrue(values[0] != values[1]);
    }
}