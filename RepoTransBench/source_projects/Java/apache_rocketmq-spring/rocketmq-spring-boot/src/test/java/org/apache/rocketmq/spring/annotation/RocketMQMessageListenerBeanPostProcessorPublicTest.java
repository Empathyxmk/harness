package org.apache.rocketmq.spring.annotation;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class RocketMQMessageListenerBeanPostProcessorPublicTest {
    @Test
    public void testSupportsBeanWithPublicData() {
        RocketMQMessageListenerBeanPostProcessor processor = new RocketMQMessageListenerBeanPostProcessor();
        Object mockBean = new Object() {
            @RocketMQMessageListener(topic = "pubTestTopic", consumerGroup = "pubGroup")
            public void listenPublic(String message) { }
        };

        assertFalse(processor.postProcessAfterInitialization(mockBean, "someOtherBean") instanceof RocketMQMessageListener);
    }
}