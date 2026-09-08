package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Message {
    String text;

    public Message(String text) { this.text = text; }
}

public class PublicMessagesTest {

    @Test
    void testMessageNotNull() {
        Message m = new Message("hi");
        assertNotNull(m.text);
    }

    @Test
    void testEmptyMessage() {
        Message m = new Message("");
        assertEquals("", m.text);
    }
}