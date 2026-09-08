package org.apache.rocketmq.spring.support;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class RocketMQUtilPublicTest {

    @Test
    public void testDefaultCharsetConstantIsUTF8() {
        assertEquals("UTF-8", RocketMQUtil.DEFAULT_CHARSET.name());
    }
}