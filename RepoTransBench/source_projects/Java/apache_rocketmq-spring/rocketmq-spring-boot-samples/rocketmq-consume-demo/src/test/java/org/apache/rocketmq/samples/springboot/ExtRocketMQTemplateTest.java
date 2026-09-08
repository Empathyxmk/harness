package org.apache.rocketmq.samples.springboot;

import org.junit.jupiter.api.Test;

public class ExtRocketMQTemplateTest {

    @Test
    public void testExtRocketMQTemplateInstantiation() {
        ExtRocketMQTemplate template = new ExtRocketMQTemplate();
        // Just instantiation test, as ExtRocketMQTemplate has no complex logic
        assert template != null;
    }
}