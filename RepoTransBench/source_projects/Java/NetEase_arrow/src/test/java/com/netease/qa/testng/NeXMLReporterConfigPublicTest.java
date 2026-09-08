package com.netease.qa.testng;

import org.junit.*;

public class NeXMLReporterConfigPublicTest {
    @Test
    public void testConfigConstantsWithDifferentAccessPattern() {
        // We re-use the constants but with assertions in a different order or style
        Assert.assertTrue(NeXMLReporterConfig.ATTR_AUTHOR.equals("author"));
        Assert.assertEquals("testName", NeXMLReporterConfig.ATTR_TC_NAME);
        Assert.assertEquals("suiteName", NeXMLReporterConfig.ATTR_TC_SUITES);
    }
}