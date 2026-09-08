package com.example.kafkaservice;

public class KafkaService {

    public String processMessage(String message) {
        if (message == null || message.trim().isEmpty()) {
            return "Error: Message cannot be empty.";
        }
        if (message.length() > 50) {
            return "Warning: Message too long.";
        }
        return "Processed: " + message.toUpperCase();
    }

    public int getMessageLength(String message) {
        if (message == null) {
            return 0;
        }
        return message.length();
    }
}