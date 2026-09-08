package com.fengsp.sender.publictests;

import org.junit.jupiter.api.Test;
import com.fengsp.sender.*;

import java.util.*;

public class PublicMessageTestCase implements PublicBaseTestCase {

    @Test
    public void testSubjectDifferent() {
        Message msg = new Message("hello");
        assert_equal(msg.getSubject(), "hello");
        msg = new Message("hello", "user1@test.com", "user2@test.com");
        assert_in(msg.getSubject(), msg.toString());
    }

    @Test
    public void testToDifferent() {
        Message msg = new Message("alice@site.com", "bob@site.com");
        assert_equal(new HashSet<>(Arrays.asList("bob@site.com")), msg.getTo());
        assert_in("bob@site.com", msg.toString());
        msg = new Message(null, null, Arrays.asList("eve@company.com", "mallory@company.com"));
        assert_equal(
            new HashSet<>(Arrays.asList("eve@company.com", "mallory@company.com")),
            msg.getTo()
        );
    }

    @Test
    public void testFromaddrDifferent() {
        Message msg = new Message("start@host.com", "end@host.com");
        assert_equal("start@host.com", msg.getFromaddr());
        assert_in("start@host.com", msg.toString());
        msg = new Message();
        msg.setFromaddr(new String[]{"Other", "other@domain.com"});
        assert_in("<other@domain.com>", msg.toString());
    }

    @Test
    public void testCcDifferent() {
        Message msg = new Message("one@test.com", "two@test.com", null, "cc2@cool.com");
        assert_in("cc2@cool.com", msg.toString());
    }

    @Test
    public void testBccDifferent() {
        Message msg = new Message("one2@test.com", "two2@test.com", null, null, "secret2@test.com");
        assert_not_in("secret2@test.com", msg.toString());
    }

    @Test
    public void testReplyToDifferent() {
        Message msg = new Message("f1@test.com", "f2@test.com", null, null, null, "response@test.com");
        assert_equal("response@test.com", msg.getReplyTo());
        assert_in("response@test.com", msg.toString());
    }

    @Test
    public void testProcessAddressDifferent() {
        Message msg = new Message(new String[]{"X\r\n", "x\r\n@foo.com"}, "y\r@foo.com", null, null, null, "z\n@foo.com");
        assert_in("<x@foo.com>", msg.toString());
        assert_in("y@foo.com", msg.toString());
        assert_in("z@foo.com", msg.toString());
    }

    @Test
    public void testCharsetDifferent() {
        Message msg = new Message();
        assert_equal("utf-8", msg.getCharset());
        msg = new Message(null, null, null, null, null, null, "latin-1");
        assert_equal("latin-1", msg.getCharset());
    }

    @Test
    public void testExtraHeadersDifferent() {
        Map<String, String> headers = new HashMap<>();
        headers.put("X-Test-Header-2", "AnotherTest");
        Message msg = new Message("aaa@bbb.com", "ccc@ddd.com", null, null, null, null, null, null, null, headers);
        assert_in("X-Test-Header-2: AnotherTest", msg.toString());
    }

    @Test
    public void testMailAndRcptOptionsDifferent() {
        Message msg = new Message();
        assert_equal(Collections.emptyList(), msg.getMailOptions());
        assert_equal(Collections.emptyList(), msg.getRcptOptions());
        msg = new Message(null, null, null, null, null, null, null, Arrays.asList("SOME_SPECIAL=ENABLED"), null);
        assert_equal(Arrays.asList("SOME_SPECIAL=ENABLED"), msg.getMailOptions());
        msg = new Message(null, null, null, null, null, null, null, null, Arrays.asList("INFO=YES"));
        assert_equal(Arrays.asList("INFO=YES"), msg.getRcptOptions());
    }

    @Test
    public void testToAddrsDifferent() {
        Message msg = new Message(null, null, "solo@place.net");
        assert_equal(new HashSet<>(Arrays.asList("solo@place.net")), msg.getToAddrs());

        msg = new Message("to@abc.com", null, Arrays.asList("to@abc.com"),
                          "xyz@def.com", null, null, null, null, Arrays.asList("hidden@abc.com", "hidden2@abc.com"));
        Set<String> expected = new HashSet<>(Arrays.asList("to@abc.com", "xyz@def.com", "hidden@abc.com", "hidden2@abc.com"));
        assert_equal(expected, msg.getToAddrs());

        msg = new Message("unique@x.com", null, null, "unique@x.com");
        assert_equal(new HashSet<>(Arrays.asList("unique@x.com")), msg.getToAddrs());
    }

    @Test
    public void testValidateDifferent() {
        Message msg = new Message("onlyfrom@fail.com", null);
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });

        msg = new Message(null, "onlyto@fail.com");
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });

        msg = new Message("from@bad.com", "to@bad.com", null, null, null, null, "bad\r");
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });
        msg = new Message("from@bad.com", "to@bad.com", null, null, null, null, "bad\n");
        assert_raises(SenderError.class, () -> {
            msg.validate();
        });
    }

    @Test
    public void testAttachDifferent() {
        Message msg = new Message();
        Attachment att = new Attachment("public.txt");
        List<Attachment> atts = Arrays.asList(new Attachment("a1.pdf"), new Attachment("b2.pdf"));
        msg.attach(att);
        assert_equal(Collections.singletonList(att), msg.getAttachments());
        msg.attach(atts);
        List<Attachment> allAtts = new ArrayList<>();
        allAtts.add(att);
        allAtts.addAll(atts);
        assert_equal(allAtts, msg.getAttachments());
    }

    @Test
    public void testAttachAttachmentDifferent() {
        Message msg = new Message();
        msg.attachAttachment("data.csv", "application/csv", "header1,header2\n1,2");
        assert_equal("data.csv", msg.getAttachments().get(0).getFilename());
        assert_equal("application/csv", msg.getAttachments().get(0).getContentType());
        assert_equal("header1,header2\n1,2", msg.getAttachments().get(0).getData());
    }

    @Test
    public void testPlainTextDifferent() {
        String plainText = "Greetings!\nThis is a public test.";
        Message msg = new Message("person@host.com", "person2@host.com", null, null, null, null, null, null, null, null, plainText);
        assert_equal(plainText, msg.getBody());
        assert_in("Greetings!", msg.getBody());
        assert_in(plainText, msg.toString());
    }
}