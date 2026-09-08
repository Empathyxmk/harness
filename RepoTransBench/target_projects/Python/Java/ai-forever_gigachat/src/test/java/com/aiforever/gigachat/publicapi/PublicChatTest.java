package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ChatMessage {
    String role;
    String content;

    public ChatMessage(String role, String content) {
        this.role = role;
        this.content = content;
    }
}

public class PublicChatTest {

    @Test
    void testSimpleChatMessage() {
        ChatMessage m = new ChatMessage("user", "What is Java?");
        assertEquals("user", m.role);
        assertTrue(m.content.contains("Java"));
    }

    @Test
    void testAssistantRoleChat() {
        ChatMessage m = new ChatMessage("assistant", "Java is a programming language.");
        assertEquals("assistant", m.role);
        assertTrue(m.content.contains("language"));
    }
}