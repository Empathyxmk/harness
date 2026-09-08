package org.apache.rocketmq.samples.springboot.consumer;

import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.Arrays;
import java.util.List;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

public class StringConsumerPublicTest {

    private RocketMQTemplate rocketMQTemplate;
    private StringConsumer stringConsumer;

    @BeforeEach
    public void setUp() {
        rocketMQTemplate = mock(RocketMQTemplate.class);
        stringConsumer = new StringConsumer();
        ReflectionTestUtils.setField(stringConsumer, "rocketMQTemplate", rocketMQTemplate);

        List<String> fakeMessages = Arrays.asList("foo", "bar", "baz");
        when(rocketMQTemplate.receive(String.class)).thenReturn(fakeMessages);
    }

    @Test
    public void testConsume() {
        List<String> messages = stringConsumer.consume();
        assertEquals(3, messages.size());
        assertTrue(messages.contains("foo"));
        assertEquals("bar", messages.get(1));
        verify(rocketMQTemplate, times(1)).receive(String.class);
    }
}