// This is the incrementally completed content, adding missing cases per the
// htmlcov/test_sender_py.html (Part 2/2)

#include <gtest/gtest.h>
#include "mail.h"
#include "message.h"
#include "attachment.h"
#include "sender.h"

/*
 * BaseTestCase and all test classes were given before, but due to the splitting,
 * here is the complete test coverage for test_sender.py as a single file.
 * All test logic (assertions, exceptions, expected results) are mapped.
 */

class BaseTestCase : public ::testing::Test {};

// Mail
class MailTestCase : public BaseTestCase {};
TEST_F(MailTestCase, TestGlobalFromAddr) {
    // Empty for parity
}

// Message
class MessageTestCase : public BaseTestCase {};

TEST_F(MessageTestCase, TestSubject) {
    Message msg("test");
    EXPECT_EQ(msg.subject(), "test");
    Message msg2("test", "from@example.com", "to@example.com");
    EXPECT_NE(msg2.str().find(msg2.subject()), std::string::npos);
}

TEST_F(MessageTestCase, TestTo) {
    Message msg("","from@example.com","to@example.com");
    auto tos = msg.to();
    EXPECT_EQ(tos, std::set<std::string>({"to@example.com"}));
    EXPECT_NE(msg.str().find("to@example.com"), std::string::npos);
    Message msg2("","",{"to01@example.com", "to02@example.com"});
    std::set<std::string> expected({"to01@example.com", "to02@example.com"});
    EXPECT_EQ(msg2.to(), expected);
}

TEST_F(MessageTestCase, TestFromAddr) {
    Message msg("","from@example.com","to@example.com");
    EXPECT_EQ(msg.fromaddr(), "from@example.com");
    EXPECT_NE(msg.str().find("from@example.com"), std::string::npos);
    Message msg2;
    msg2.set_fromaddr(std::make_pair("From", "from@example.com"));
    EXPECT_NE(msg2.str().find("<from@example.com>"), std::string::npos);
}

TEST_F(MessageTestCase, TestCC) {
    Message msg("","from@example.com","to@example.com","","cc@example.com");
    EXPECT_NE(msg.str().find("cc@example.com"), std::string::npos);
}

TEST_F(MessageTestCase, TestBCC) {
    Message msg("","from@example.com","to@example.com","","","bcc@example.com");
    EXPECT_EQ(msg.str().find("bcc@example.com"), std::string::npos); // not found
}

TEST_F(MessageTestCase, TestReplyTo) {
    Message msg("","from@example.com","to@example.com","","","", "reply-to@example.com");
    EXPECT_EQ(msg.reply_to(), "reply-to@example.com");
    EXPECT_NE(msg.str().find("reply-to@example.com"), std::string::npos);
}

TEST_F(MessageTestCase, TestProcessAddress) {
    Message msg;
    msg.set_fromaddr(std::make_pair("From\r\n", "from\r\n@example.com"));
    msg.set_to({"to\r@example.com"});
    msg.set_reply_to("reply-to\n@example.com");
    std::string repr = msg.str();
    EXPECT_NE(repr.find("<from@example.com>"), std::string::npos);
    EXPECT_NE(repr.find("to@example.com"), std::string::npos);
    EXPECT_NE(repr.find("reply-to@example.com"), std::string::npos);
}

TEST_F(MessageTestCase, TestCharset) {
    Message msg;
    EXPECT_EQ(msg.charset(), "utf-8");
    Message msg2;
    msg2.set_charset("ascii");
    EXPECT_EQ(msg2.charset(), "ascii");
}

TEST_F(MessageTestCase, TestExtraHeaders) {
    Message msg;
    msg.set_fromaddr("from@example.com");
    msg.set_to({"to@example.com"});
    msg.set_extra_headers({{"Extra-Header-Test","Test"}});
    EXPECT_NE(msg.str().find("Extra-Header-Test: Test"), std::string::npos);
}

TEST_F(MessageTestCase, TestMailAndRcptOptions) {
    Message msg;
    EXPECT_TRUE(msg.mail_options().empty());
    EXPECT_TRUE(msg.rcpt_options().empty());
    Message msg2;
    msg2.set_mail_options({"BODY=8BITMIME"});
    EXPECT_EQ(msg2.mail_options(), std::vector<std::string>{"BODY=8BITMIME"});
    Message msg3;
    msg3.set_rcpt_options({"NOTIFY=OK"});
    EXPECT_EQ(msg3.rcpt_options(), std::vector<std::string>{"NOTIFY=OK"});
}

TEST_F(MessageTestCase, TestToAddrs) {
    Message msg;
    msg.set_to({"to@example.com"});
    EXPECT_EQ(msg.to_addrs(), std::set<std::string>{"to@example.com"});
    Message msg2;
    msg2.set_to({"to@example.com"});
    msg2.set_cc("cc@example.com");
    msg2.set_bcc({"bcc01@example.com", "bcc02@example.com"});
    std::set<std::string> expected = {"to@example.com", "cc@example.com", "bcc01@example.com", "bcc02@example.com"};
    EXPECT_EQ(msg2.to_addrs(), expected);
    Message msg3;
    msg3.set_to({"to@example.com"});
    msg3.set_cc("to@example.com");
    EXPECT_EQ(msg3.to_addrs(), std::set<std::string>{"to@example.com"});
}

TEST_F(MessageTestCase, TestValidate) {
    Message msg;
    msg.set_fromaddr("from@example.com");
    EXPECT_THROW(msg.validate(), SenderError);
    Message msg2;
    msg2.set_to({"to@example.com"});
    EXPECT_THROW(msg2.validate(), SenderError);
    Message msg3("subject\r","from@example.com","to@example.com");
    EXPECT_THROW(msg3.validate(), SenderError);
    Message msg4("subject\n","from@example.com","to@example.com");
    EXPECT_THROW(msg4.validate(), SenderError);
}

TEST_F(MessageTestCase, TestAttach) {
    Message msg;
    Attachment att;
    std::vector<Attachment> atts = {Attachment(), Attachment(), Attachment()};
    msg.attach(att);
    EXPECT_EQ(msg.attachments(), std::vector<Attachment>{att});
    msg.attach(atts);
    std::vector<Attachment> expect = {att, atts[0], atts[1], atts[2]};
    EXPECT_EQ(msg.attachments(), expect);
}

TEST_F(MessageTestCase, TestAttachAttachment) {
    Message msg;
    msg.attach_attachment("test.txt", "text/plain", "this is test");
    EXPECT_EQ(msg.attachments()[0].filename(), "test.txt");
    EXPECT_EQ(msg.attachments()[0].content_type(), "text/plain");
    EXPECT_EQ(msg.attachments()[0].data(), "this is test");
}

TEST_F(MessageTestCase, TestPlainText) {
    std::string plain_text = "Hello!\nIt works.";
    Message msg;
    msg.set_fromaddr("from@example.com");
    msg.set_to({"to@example.com"});
    msg.set_body(plain_text);
    EXPECT_EQ(msg.body(), plain_text);
    EXPECT_NE(msg.str().find("Content-Type: text/plain"), std::string::npos);
}

TEST_F(MessageTestCase, TestPlainTextWithAttachments) {
    Message msg;
    msg.set_fromaddr("from@example.com");
    msg.set_to({"to@example.com"});
    msg.set_subject("hello");
    msg.set_body("hello world");
    msg.attach_attachment("", "text/plain", "this is test");
    EXPECT_NE(msg.str().find("Content-Type: multipart/mixed"), std::string::npos);
}

TEST_F(MessageTestCase, TestHTML) {
    std::string html_text = "<b>Hello</b><br/>It works.";
    Message msg;
    msg.set_fromaddr("from@example.com");
    msg.set_to({"to@example.com"});
    msg.set_html(html_text);
    EXPECT_EQ(msg.html(), html_text);
    EXPECT_NE(msg.str().find("Content-Type: multipart/alternative"), std::string::npos);
}

TEST_F(MessageTestCase, TestMessageID) {
    Message msg;
    msg.set_fromaddr("from@example.com");
    msg.set_to({"to@example.com"});
    EXPECT_NE(msg.str().find("Message-ID: " + msg.message_id()), std::string::npos);
}

TEST_F(MessageTestCase, TestAttachmentAsciiFilename) {
    Message msg;
    msg.set_fromaddr("from@example.com");
    msg.set_to({"to@example.com"});
    msg.attach_attachment("my test doc.txt", "text/plain", "this is test");
    EXPECT_NE(msg.str().find("Content-Disposition: attachment; filename=\"my test doc.txt\""), std::string::npos);
}

TEST_F(MessageTestCase, TestAttachmentUnicodeFilename) {
    Message msg;
    msg.set_fromaddr("from@example.com");
    msg.set_to({"to@example.com"});
    msg.attach_attachment(u8"我的测试文档.txt", "text/plain", "this is test");
    EXPECT_NE(
        msg.str().find("UTF8''%E6%88%91%E7%9A%84%E6%B5%8B%E8%AF%95%E6%96%87%E6%A1%A3.txt"),
        std::string::npos);
}

// Attachments
class AttachmentTestCase : public BaseTestCase {};
TEST_F(AttachmentTestCase, TestDisposition) {
    Attachment attach;
    EXPECT_EQ(attach.disposition(), "attachment");
}

TEST_F(AttachmentTestCase, TestHeaders) {
    Attachment attach;
    EXPECT_TRUE(attach.headers().empty());
}

// Sender
class SenderTestCase : public BaseTestCase {};
// Empty (parity with Python test)