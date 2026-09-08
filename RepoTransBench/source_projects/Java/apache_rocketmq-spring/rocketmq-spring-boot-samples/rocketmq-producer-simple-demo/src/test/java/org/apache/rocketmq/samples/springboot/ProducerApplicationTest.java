package org.apache.rocketmq.samples.springboot;

import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.test.util.ReflectionTestUtils;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class ProducerApplicationTest {

    private RocketMQTemplate rocketMQTemplate;
    private ProducerApplication producerApplication;

    @BeforeEach
    public void setup() {
        rocketMQTemplate = mock(RocketMQTemplate.class);
        producerApplication = new ProducerApplication();

        // Using ReflectionTestUtils to set private fields
        ReflectionTestUtils.setField(producerApplication, "rocketMQTemplate", rocketMQTemplate);
        ReflectionTestUtils.setField(producerApplication, "topic", "testTopic");

        SendResult mockResult = mock(SendResult.class);
        when(rocketMQTemplate.syncSend(anyString(), any())).thenReturn(mockResult);
    }

    @Test
    public void testRun() {
        producerApplication.run();
        verify(rocketMQTemplate, times(1)).syncSend(eq("testTopic"), eq("Hello, World!"));
    }

    @Test
    public void testMain() {
        // Covers the main method for coverage
        SpringApplication mockApp = mock(SpringApplication.class);
        String[] args = new String[0];
        ProducerApplication.main(args);
    }
}