package com.fengsp.sender.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

import com.fengsp.sender.*;

// This class represents additional synthetic coverage-based tests as captured in htmlcov/test_sender_py.html.
// It mainly duplicates and enhances already present scenarios,
// but ensures complete parity with coverage expectations.
public class HtmlCoverageTestSenderPy implements BaseTestCase {

    @Test
    void testAttachAttachment() {
        Message msg = new Message();
        msg.attachAttachment("test.txt", "text/plain", "this is test");
        assert_equal("test.txt", msg.getAttachments().get(0).getFilename());
        assert_equal("text/plain", msg.getAttachments().get(0).getContentType());
        assert_equal("this is test", msg.getAttachments().get(0).getData());
    }

    @Test
    void testPlainText() {
        String plainText = "Hello!\nIt works.";
        Message msg = new Message("from@example.com", "to@example.com", null, null, null, null, null, null, null, null, plainText);
        assert_equal(plainText, msg.getBody());
        assert_in("Content-Type: text/plain", msg.toString());
    }

    @Test
    void testPlainTextWithAttachments() {
        Message msg = new Message("from@example.com", "to@example.com", "hello", null, null, null, null, null, null, null, "hello world");
        msg.attachAttachment(null, "text/plain", "this is test".getBytes());
        assert_in("Content-Type: multipart/mixed", msg.toString());
    }

    @Test
    void testHtml() {
        String htmlText = "<b>Hello</b><br/>It works.";
        Message msg = new Message("from@example.com", "to@example.com", null, null, null, null, null, null, null, null, null, htmlText);
        assert_equal(htmlText, msg.getHtml());
        assert_in("Content-Type: multipart/alternative", msg.toString());
    }

    @Test
    void testMessageId() {
        Message msg = new Message("from@example.com", "to@example.com");
        assert_in("Message-ID: " + msg.getMessageId(), msg.toString());
    }

    @Test
    void testAttachmentAsciiFilename() {
        Message msg = new Message("from@example.com", "to@example.com");
        msg.attachAttachment("my test doc.txt", "text/plain", "this is test".getBytes());
        assert_in("Content-Disposition: attachment; filename=\"my test doc.txt\"", msg.toString());
    }

    @Test
    void testAttachmentUnicodeFilename() {
        Message msg = new Message("from@example.com", "to@example.com");
        msg.attachAttachment("我的测试文档.txt", "text/plain", "this is test");
        assert_in("UTF8''%E6%88%91%E7%9A%84%E6%B5%8B%E8%AF%95%E6%96%87%E6%A1%A3.txt", msg.toString());
    }

    @Test
    void testAttachmentTestCase_Disposition() {
        Attachment attach = new Attachment();
        assert_equal(attach.getDisposition(), "attachment");
    }

    @Test
    void testAttachmentTestCase_Headers() {
        Attachment attach = new Attachment();
        assert_equal(attach.getHeaders(), new HashMap<String, String>());
    }
}