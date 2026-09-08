package org.apache.rocketmq.spring.support;

import org.junit.jupiter.api.Test;

public class DefaultRocketMQListenerContainerPublicTest {

    @Test
    public void testDefaultLifecycleBehavior() {
        DefaultRocketMQListenerContainer container = new DefaultRocketMQListenerContainer();
        container.setName("publicContainer");
        // We're simply testing initialization for coverage (public data name)
        assert !container.isRunning();
    }
}