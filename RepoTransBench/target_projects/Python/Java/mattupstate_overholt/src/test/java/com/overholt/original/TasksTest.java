package com.overholt.original;

import com.overholt.tasks.Tasks;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

class TasksTest {

    @Test
    void testSendManagerAddedEmailPrints() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outContent));
        try {
            Tasks.sendManagerAddedEmail("user1@example.com", "user2@example.com");
            System.out.flush();
            String output = outContent.toString();
            assertTrue(output.contains("sending manager added email"));
        } finally {
            System.setOut(originalOut);
        }
    }

    @Test
    void testSendManagerRemovedEmailPrints() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outContent));
        try {
            Tasks.sendManagerRemovedEmail("user3@example.com");
            System.out.flush();
            String output = outContent.toString();
            assertTrue(output.contains("sending manager removed email"));
        } finally {
            System.setOut(originalOut);
        }
    }
}