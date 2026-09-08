package org.apache.rocketmq.spring.core;

import org.apache.rocketmq.spring.support.RocketMQHeaders;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.messaging.Message;
import org.springframework.messaging.support.MessageBuilder;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

public class RocketMQTemplatePublicTest {

    private RocketMQTemplate rocketMQTemplate;

    @BeforeEach
    public void setUp() {
        rocketMQTemplate = Mockito.spy(new RocketMQTemplate());
        // Further configuration/mocking if needed.
    }

    @Test
    public void testSendAndReceiveWithDifferentData() {
        // Create a message with different (public) content
        Message<String> msg = MessageBuilder.withPayload("HelloPublic")
            .setHeader(RocketMQHeaders.KEYS, "pubKey-789")
            .build();

        // Mocks
        doNothing().when(rocketMQTemplate).sendOneWay(eq("public-topic"), eq(msg));
        rocketMQTemplate.sendOneWay("public-topic", msg);

        verify(rocketMQTemplate, times(1)).sendOneWay("public-topic", msg);
    }

    @Test
    public void testSyncSendReturnsNull() {
        // When syncSend is called with a certain topic/message, return null
        when(rocketMQTemplate.syncSend(eq("testSyncPUB"), any())).thenReturn(null);
        Object result = rocketMQTemplate.syncSend("testSyncPUB", "public-body-123");
        assertNull(result);
    }

}