package com.netease.qa.testng;

import org.junit.*;

public class NeXMLReporterConfigTest {
    @Test
    public void testConfigConstants() {
        Assert.assertEquals("testName", NeXMLReporterConfig.ATTR_TC_NAME);
        Assert.assertEquals("suiteName", NeXMLReporterConfig.ATTR_TC_SUITES);
        Assert.assertEquals("author", NeXMLReporterConfig.ATTR_AUTHOR);
    }
}