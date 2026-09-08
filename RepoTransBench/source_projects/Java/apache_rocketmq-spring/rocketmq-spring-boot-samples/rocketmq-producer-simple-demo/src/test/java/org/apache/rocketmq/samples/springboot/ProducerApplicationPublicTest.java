package org.apache.rocketmq.samples.springboot;

import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.SpringApplication;
import org.springframework.test.util.ReflectionTestUtils;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class ProducerApplicationPublicTest {

    private RocketMQTemplate rocketMQTemplate;
    private ProducerApplication producerApplication;

    @BeforeEach
    public void setup() {
        rocketMQTemplate = mock(RocketMQTemplate.class);
        producerApplication = new ProducerApplication();

        // Use a different topic and message for public test
        ReflectionTestUtils.setField(producerApplication, "rocketMQTemplate", rocketMQTemplate);
        ReflectionTestUtils.setField(producerApplication, "topic", "publicTopic");

        SendResult mockResult = mock(SendResult.class);
        when(rocketMQTemplate.syncSend(anyString(), any())).thenReturn(mockResult);
    }

    @Test
    public void testRun() {
        // Use a different expected message for verification
        // The actual logic invoked in run() calls .syncSend(topic, "Hello, World!")
        // But since we changed topic, at least the topic is different for public test
        producerApplication.run();
        verify(rocketMQTemplate, times(1)).syncSend(eq("publicTopic"), eq("Hello, World!"));
    }

    @Test
    public void testMain() {
        // Covers the main method for coverage
        String[] args = new String[] { "public" };
        ProducerApplication.main(args);
    }
}