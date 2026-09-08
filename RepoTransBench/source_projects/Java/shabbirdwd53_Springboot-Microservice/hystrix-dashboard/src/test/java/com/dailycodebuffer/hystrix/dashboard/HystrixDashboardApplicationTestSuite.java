package com.dailycodebuffer.hystrix.dashboard;

import org.junit.Test;
import org.junit.Assert;
import org.springframework.boot.SpringApplication;

public class HystrixDashboardApplicationTestSuite {

    @Test
    public void testMainMethod() {
        // This test calls main to get line coverage for SpringApplication.run
        HystrixDashboardApplication.main(new String[]{"--spring.profiles.active=test"});
    }

    @Test
    public void testNoArgsMain() {
        // This is an edge case: main with null args
        HystrixDashboardApplication.main(null);
    }
}