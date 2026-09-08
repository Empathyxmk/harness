package com.example.kafkaservice;

import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class KafkaServiceTest {

    @Test
    public void testProcessMessage_valid() {
        KafkaService service = new KafkaService();
        String result = service.processMessage("hello world");
        assertNotNull(result);
        assertEquals("Processed: HELLO WORLD", result);
    }

    @Test
    public void testProcessMessage_null() {
        KafkaService service = new KafkaService();
        String result = service.processMessage(null);
        assertNotNull(result);
        assertEquals("Error: Message cannot be empty.", result);
    }

    @Test
    public void testProcessMessage_empty() {
        KafkaService service = new KafkaService();
        String result = service.processMessage("");
        assertNotNull(result);
        assertEquals("Error: Message cannot be empty.", result);
    }

    @Test
    public void testProcessMessage_whitespace() {
        KafkaService service = new KafkaService();
        String result = service.processMessage("   ");
        assertNotNull(result);
        assertEquals("Error: Message cannot be empty.", result);
    }

    @Test
    public void testProcessMessage_tooLong() {
        KafkaService service = new KafkaService();
        String longMessage = "This is a very long message that definitely exceeds fifty characters in length and will trigger the warning message condition.";
        String result = service.processMessage(longMessage);
        assertNotNull(result);
        assertEquals("Warning: Message too long.", result);
    }

    @Test
    public void testProcessMessage_boundaryLengthFifty() {
        KafkaService service = new KafkaService();
        String fiftyCharMessage = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX"; // 50 chars
        String result = service.processMessage(fiftyCharMessage);
        assertNotNull(result);
        assertEquals("Processed: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWX", result);
    }

    @Test
    public void testProcessMessage_boundaryLengthFiftyOne() {
        KafkaService service = new KafkaService();
        String fiftyOneCharMessage = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY"; // 51 chars
        String result = service.processMessage(fiftyOneCharMessage);
        assertNotNull(result);
        assertEquals("Warning: Message too long.", result);
    }


    @Test
    public void testGetMessageLength_valid() {
        KafkaService service = new KafkaService();
        int length = service.getMessageLength("test");
        assertEquals(4, length);
    }

    @Test
    public void testGetMessageLength_null() {
        KafkaService service = new KafkaService();
        int length = service.getMessageLength(null);
        assertEquals(0, length);
    }

    @Test
    public void testGetMessageLength_empty() {
        KafkaService service = new KafkaService();
        int length = service.getMessageLength("");
        assertEquals(0, length);
    }
}