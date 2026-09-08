package org.apache.rocketmq.samples.springboot;

import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.Arrays;
import java.util.List;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

public class ExtRocketMQTemplatePublicTest {

    private RocketMQTemplate rocketMQTemplate;
    private ExtRocketMQTemplate extRocketMQTemplate;

    @BeforeEach
    public void setUp() {
        rocketMQTemplate = mock(RocketMQTemplate.class);
        extRocketMQTemplate = new ExtRocketMQTemplate();
        ReflectionTestUtils.setField(extRocketMQTemplate, "rocketMQTemplate", rocketMQTemplate);

        List<String> mockResult = Arrays.asList("alpha", "beta", "gamma");
        when(rocketMQTemplate.receive(String.class)).thenReturn(mockResult);
    }

    @Test
    public void testReceiveMessage() {
        List<String> received = extRocketMQTemplate.receiveMessage();
        assertEquals(3, received.size());
        assertEquals("alpha", received.get(0));
        assertTrue(received.contains("beta"));
        verify(rocketMQTemplate, times(1)).receive(String.class);
    }
}