package com.fengsp.sender.publictests;

import com.fengsp.sender.Attachment;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicAttachmentTestCase {
    @Test
    public void testAttachmentCreationDifferentFile() {
        Attachment a = new Attachment("newfile.pdf");
        assertEquals("newfile.pdf", a.getFilename());
        assertNotNull(a);
    }

    @Test
    public void testAttachmentReprDifferentFile() {
        Attachment a = new Attachment("readme.md");
        assertTrue(a.toString().contains("Attachment"));
    }
}