package com.dailycodebuffer.cloud.gateway;

import org.junit.platform.runner.JUnitPlatform;
import org.junit.platform.suite.api.SelectClasses;
import org.junit.runner.RunWith;

@RunWith(JUnitPlatform.class)
@SelectClasses({
    CloudGatewayApplicationTests.class,
    FallBackMethodControllerTest.class
})
public class CloudGatewayApplicationTestSuite {}