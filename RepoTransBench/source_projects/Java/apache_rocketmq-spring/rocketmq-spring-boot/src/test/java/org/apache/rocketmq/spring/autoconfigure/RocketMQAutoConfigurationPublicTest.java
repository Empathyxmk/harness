package org.apache.rocketmq.spring.autoconfigure;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class RocketMQAutoConfigurationPublicTest {

    @Test
    public void testInstantiateAutoConfig() {
        RocketMQAutoConfiguration config = new RocketMQAutoConfiguration();
        assertNotNull(config);
    }
}