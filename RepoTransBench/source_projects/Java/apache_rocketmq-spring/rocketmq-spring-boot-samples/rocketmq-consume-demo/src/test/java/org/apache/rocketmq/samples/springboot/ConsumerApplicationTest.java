package org.apache.rocketmq.samples.springboot;

import org.apache.rocketmq.spring.core.RocketMQTemplate;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.SpringApplication;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.Arrays;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

public class ConsumerApplicationTest {

    private RocketMQTemplate rocketMQTemplate;
    private RocketMQTemplate extRocketMQTemplate;
    private ConsumerApplication consumerApplication;

    @BeforeEach
    public void setup() {
        rocketMQTemplate = mock(RocketMQTemplate.class);
        extRocketMQTemplate = mock(RocketMQTemplate.class);
        consumerApplication = new ConsumerApplication();

        List<String> mockList = Arrays.asList("msg1", "msg2");
        when(rocketMQTemplate.receive(String.class)).thenReturn(mockList);
        when(extRocketMQTemplate.receive(String.class)).thenReturn(mockList);

        ReflectionTestUtils.setField(consumerApplication, "rocketMQTemplate", rocketMQTemplate);
        ReflectionTestUtils.setField(consumerApplication, "extRocketMQTemplate", extRocketMQTemplate);
    }

    @Test
    public void testRun() throws Exception {
        consumerApplication.run();
        verify(rocketMQTemplate, times(1)).receive(String.class);
        verify(extRocketMQTemplate, times(1)).receive(String.class);
    }

    @Test
    public void testMain() {
        String[] args = new String[0];
        ConsumerApplication.main(args);
    }
}