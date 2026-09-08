package com.dailycodebuffer.service.registry;

import org.junit.Test;

public class ServiceRegistryApplicationTestSuite {

    @Test
    public void testMainMethod() {
        ServiceRegistryApplication.main(new String[]{"--spring.profiles.active=test"});
    }

    @Test
    public void testNoArgsMain() {
        ServiceRegistryApplication.main(null);
    }
}