package jetbrick.template.exec.buildin;

import org.junit.Assert;
import org.junit.Test;

public class BuildinFunctionPublicTest {
    @Test
    public void testStringLengthFunctionWithDifferentString() {
        // Different string than in private/build-in tests
        String test = "alpha";
        Assert.assertEquals(5, test.length());
    }

    @Test
    public void testStringStartsWithFunctionWithDifferentPrefix() {
        String test = "framework";
        Assert.assertTrue(test.startsWith("frame"));
        Assert.assertFalse(test.startsWith("work"));
    }
}