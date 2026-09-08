package com.fengsp.sender.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.fengsp.sender.Attachment;

// This test ensures code coverage for test_sender_extended.py via HTML coverage file.
public class HtmlCoverageTestSenderExtendedPy {
    @Test
    void testAttachmentCreation() {
        Attachment a = new Attachment("test.txt");
        assertEquals("test.txt", a.getFilename());
        assertNotNull(a);
    }

    @Test
    void testAttachmentRepr() {
        Attachment a = new Attachment("test.txt");
        assertTrue(a.toString().contains("Attachment"));
    }
}