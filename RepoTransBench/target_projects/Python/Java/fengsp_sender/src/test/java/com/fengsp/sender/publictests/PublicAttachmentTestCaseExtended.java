package com.fengsp.sender.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.fengsp.sender.Attachment;

/**
 * These tests correspond to coverage details from public_test_sender_extended.py as shown in htmlcov/public_test_sender_extended_py.html.
 */
public class PublicAttachmentTestCaseExtended {

    @Test
    void testAttachmentCreationDifferentFile() {
        Attachment a = new Attachment("newfile.pdf");
        assertEquals("newfile.pdf", a.getFilename());
        assertNotNull(a);
    }

    @Test
    void testAttachmentReprDifferentFile() {
        Attachment a = new Attachment("readme.md");
        assertTrue(a.toString().contains("Attachment"));
    }
}