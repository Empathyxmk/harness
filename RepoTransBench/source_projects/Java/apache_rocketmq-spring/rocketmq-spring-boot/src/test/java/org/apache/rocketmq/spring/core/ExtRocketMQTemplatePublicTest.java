package org.apache.rocketmq.spring.core;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.messaging.Message;
import org.springframework.messaging.support.MessageBuilder;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

public class ExtRocketMQTemplatePublicTest {

    private RocketMQTemplate rocketMQTemplate;
    private ExtRocketMQTemplate extRocketMQTemplate;

    @BeforeEach
    public void setUp() {
        rocketMQTemplate = Mockito.mock(RocketMQTemplate.class);
        extRocketMQTemplate = new ExtRocketMQTemplate();
        extRocketMQTemplate.setRocketMQTemplate(rocketMQTemplate);

        when(rocketMQTemplate.syncSend(eq("pubExtTopic"), any()))
                .thenReturn(null);
        when(rocketMQTemplate.syncSend(eq("pubExtTopic"), any(Message.class)))
                .thenReturn(null);
    }

    @Test
    public void testSendStringMessage() {
        extRocketMQTemplate.sendStringMessage("pubExtTopic", "msgPublic");
        verify(rocketMQTemplate, times(1)).syncSend(eq("pubExtTopic"), eq("msgPublic"));
    }

    @Test
    public void testSendSpringMessage() {
        Message<String> springMsg = MessageBuilder.withPayload("data42").build();
        extRocketMQTemplate.sendSpringMessage("pubExtTopic", springMsg);
        verify(rocketMQTemplate, times(1)).syncSend(eq("pubExtTopic"), eq(springMsg));
    }
}