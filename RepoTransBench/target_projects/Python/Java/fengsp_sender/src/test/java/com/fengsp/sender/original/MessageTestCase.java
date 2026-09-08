package com.fengsp.sender.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.fengsp.sender.*;

import java.util.*;

public class MessageTestCase implements BaseTestCase {

    @Test
    void testSubject() {
        Message msg = new Message("test");
        assert_equal(msg.getSubject(), "test");
        msg = new Message("test", "from@example.com", "to@example.com");
        assert_in(msg.getSubject(), msg.toString());
    }

    @Test
    void testTo() {
        Message msg = new Message("from@example.com", "to@example.com");
        assert_equal(new HashSet<>(Arrays.asList("to@example.com")), msg.getTo());
        assert_in("to@example.com", msg.toString());
        msg = new Message(null, null, Arrays.asList("to01@example.com", "to02@example.com"));
        assert_equal(
            new HashSet<>(Arrays.asList("to01@example.com", "to02@example.com")),
            msg.getTo()
        );
    }

    @Test
    void testFromaddr() {
        Message msg = new Message("from@example.com", "to@example.com");
        assert_equal("from@example.com", msg.getFromaddr());
        assert_in("from@example.com", msg.toString());
        msg = new Message();
        msg.setFromaddr(new String[]{"From", "from@example.com"});
        assert_in("<from@example.com>", msg.toString());
    }

    @Test
    void testCc() {
        Message msg = new Message("from@example.com", "to@example.com", null, "cc@example.com");
        assert_in("cc@example.com", msg.toString());
    }

    @Test
    void testBcc() {
        Message msg = new Message("from@example.com", "to@example.com", null, null, "bcc@example.com");
        assert_not_in("bcc@example.com", msg.toString());
    }

    @Test
    void testReplyTo() {
        Message msg = new Message("from@example.com", "to@example.com", null, null, null, "reply-to@example.com");
        assert_equal("reply-to@example.com", msg.getReplyTo());
        assert_in("reply-to@example.com", msg.toString());
    }

    @Test
    void testProcessAddress() {
        Message msg = new Message(
                new String[]{"From\r\n", "from\r\n@example.com"},
                "to\r@example.com", null, null, null,
                "reply-to\n@example.com"
        );
        assert_in("<from@example.com>", msg.toString());
        assert_in("to@example.com", msg.toString());
        assert_in("reply-to@example.com", msg.toString());
    }

    @Test
    void testCharset() {
        Message msg = new Message();
        assert_equal("utf-8", msg.getCharset());
        msg = new Message(null, null, null, null, null, null, "ascii");
        assert_equal("ascii", msg.getCharset());
    }

    @Test
    void testExtraHeaders() {
        Map<String, String> headers = new HashMap<>();
        headers.put("Extra-Header-Test", "Test");
        Message msg = new Message("from@example.com", "to@example.com", null, null, null, null, null, null, null, headers);
        assert_in("Extra-Header-Test: Test", msg.toString());
    }

    @Test
    void testMailAndRcptOptions() {
        Message msg = new Message();
        assert_equal(Collections.emptyList(), msg.getMailOptions());
        assert_equal(Collections.emptyList(), msg.getRcptOptions());
        msg = new Message(null, null, null, null, null, null, null, Arrays.asList("BODY=8BITMIME"), null);
        assert_equal(Arrays.asList("BODY=8BITMIME"), msg.getMailOptions());
        msg = new Message(null, null, null, null, null, null, null, null, Arrays.asList("NOTIFY=OK"));
        assert_equal(Arrays.asList("NOTIFY=OK"), msg.getRcptOptions());
    }

    @Test
    void testToAddrs() {
        Message msg = new Message(null, null, "to@example.com");
        assert_equal(new HashSet<>(Arrays.asList("to@example.com")), msg.getToAddrs());

        msg = new Message("to@example.com", null, Arrays.asList("to@example.com"),
                          "cc@example.com", null, null, null, null, Arrays.asList("bcc01@example.com", "bcc02@example.com"));
        Set<String> expected = new HashSet<>(Arrays.asList("to@example.com", "cc@example.com", "bcc01@example.com", "bcc02@example.com"));
        assert_equal(expected, msg.getToAddrs());

        msg = new Message("to@example.com", null, null, "to@example.com");
        assert_equal(new HashSet<>(Arrays.asList("to@example.com")), msg.getToAddrs());
    }

    @Test
    void testValidate() {
        Message msg = new Message("from@example.com", null);
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });

        msg = new Message(null, "to@example.com");
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });

        msg = new Message("from@example.com", "to@example.com", null, null, null, null, "subject\r");
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });
        msg = new Message("from@example.com", "to@example.com", null, null, null, null, "subject\n");
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });
    }

    @Test
    void testAttach() {
        Message msg = new Message();
        Attachment att = new Attachment();
        List<Attachment> atts = Arrays.asList(new Attachment(), new Attachment(), new Attachment());
        msg.attach(att);
        assert_equal(Collections.singletonList(att), msg.getAttachments());
        msg.attach(atts);
        List<Attachment> allAtts = new ArrayList<>();
        allAtts.add(att);
        allAtts.addAll(atts);
        assert_equal(allAtts, msg.getAttachments());
    }

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
}