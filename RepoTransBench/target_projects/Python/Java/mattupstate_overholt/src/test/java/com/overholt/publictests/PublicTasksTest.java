package com.overholt.publictests;

import com.overholt.tasks.Tasks;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class PublicTasksTest {

    @Test
    void testPublicSendManagerAddedEmailContent() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outContent));
        try {
            Tasks.sendManagerAddedEmail("public1@example.com", "public2@example.com");
            System.out.flush();
            String output = outContent.toString();
            assertTrue(output.contains("manager added email"));
        } finally {
            System.setOut(originalOut);
        }
    }

    @Test
    void testPublicSendManagerRemovedEmailContent() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outContent));
        try {
            Tasks.sendManagerRemovedEmail("public3@example.com");
            System.out.flush();
            String output = outContent.toString();
            assertTrue(output.contains("manager removed email"));
        } finally {
            System.setOut(originalOut);
        }
    }
}