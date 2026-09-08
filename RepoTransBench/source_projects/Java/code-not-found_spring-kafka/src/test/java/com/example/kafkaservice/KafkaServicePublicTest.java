package com.example.kafkaservice;

import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class KafkaServicePublicTest {

    @Test
    public void testProcessMessage_valid_diff() {
        KafkaService service = new KafkaService();
        String result = service.processMessage("Kafka Rocks");
        assertNotNull(result);
        assertEquals("Processed: KAFKA ROCKS", result);
    }

    @Test
    public void testProcessMessage_null_public() {
        KafkaService service = new KafkaService();
        String result = service.processMessage(null);
        assertNotNull(result);
        assertEquals("Error: Message cannot be empty.", result);
    }

    @Test
    public void testProcessMessage_empty_public() {
        KafkaService service = new KafkaService();
        String result = service.processMessage("");
        assertNotNull(result);
        assertEquals("Error: Message cannot be empty.", result);
    }

    @Test
    public void testProcessMessage_whitespace_public() {
        KafkaService service = new KafkaService();
        String result = service.processMessage("\t\n");
        assertNotNull(result);
        assertEquals("Error: Message cannot be empty.", result);
    }

    @Test
    public void testProcessMessage_tooLong_public() {
        KafkaService service = new KafkaService();
        // This message is 55 characters long, longer than 50
        String longMessage = "Short messages are nice, but this one is way too long!!!";
        String result = service.processMessage(longMessage);
        assertNotNull(result);
        assertEquals("Warning: Message too long.", result);
    }

    @Test
    public void testProcessMessage_boundaryLengthFifty_public() {
        KafkaService service = new KafkaService();
        String msg = "12345678901234567890123456789012345678901234567890"; // 50 chars
        String result = service.processMessage(msg);
        assertNotNull(result);
        assertEquals("Processed: 12345678901234567890123456789012345678901234567890", result);
    }

    @Test
    public void testProcessMessage_boundaryLengthFiftyOne_public() {
        KafkaService service = new KafkaService();
        String msg = "123456789012345678901234567890123456789012345678901"; // 51 chars
        String result = service.processMessage(msg);
        assertNotNull(result);
        assertEquals("Warning: Message too long.", result);
    }


    @Test
    public void testGetMessageLength_valid_public() {
        KafkaService service = new KafkaService();
        int length = service.getMessageLength("Kafka");
        assertEquals(5, length);
    }

    @Test
    public void testGetMessageLength_null_public() {
        KafkaService service = new KafkaService();
        int length = service.getMessageLength(null);
        assertEquals(0, length);
    }

    @Test
    public void testGetMessageLength_empty_public() {
        KafkaService service = new KafkaService();
        int length = service.getMessageLength("   ".trim());
        assertEquals(0, length);
    }
}