package com.fengsp.sender.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.fengsp.sender.Attachment;

public class AttachmentTestCase2 implements BaseTestCase {

    @Test
    void testDisposition() {
        Attachment attach = new Attachment();
        assert_equal(attach.getDisposition(), "attachment");
    }

    @Test
    void testHeaders() {
        Attachment attach = new Attachment();
        assert_equal(attach.getHeaders(), new java.util.HashMap<>());
    }
}