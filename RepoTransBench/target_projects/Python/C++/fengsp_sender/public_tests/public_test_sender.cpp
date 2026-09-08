#include <gtest/gtest.h>
#include "mail.h"
#include "message.h"
#include "attachment.h"
#include "sender.h"

class PublicBaseTestCase : public ::testing::Test {};

// Mail
class PublicMailTestCase : public PublicBaseTestCase {};
TEST_F(PublicMailTestCase, TestGlobalFromAddrAlternate) {
    // No logic in original Python, maintain parity for coverage
}

// Message
class PublicMessageTestCase : public PublicBaseTestCase {};

TEST_F(PublicMessageTestCase, TestSubjectDifferent) {
    Message msg("hello");
    EXPECT_EQ(msg.subject(), "hello");
    Message msg2("hello", "user1@test.com", "user2@test.com");
    EXPECT_NE(msg2.str().find(msg2.subject()), std::string::npos);
}

TEST_F(PublicMessageTestCase, TestToDifferent) {
    Message msg("","alice@site.com","bob@site.com");
    EXPECT_EQ(msg.to(), std::set<std::string>({"bob@site.com"}));
    EXPECT_NE(msg.str().find("bob@site.com"), std::string::npos);
    Message msg2("","",{"eve@company.com", "mallory@company.com"});
    std::set<std::string> expected({"eve@company.com", "mallory@company.com"});
    EXPECT_EQ(msg2.to(), expected);
}

TEST_F(PublicMessageTestCase, TestFromAddrDifferent) {
    Message msg("","start@host.com","end@host.com");
    EXPECT_EQ(msg.fromaddr(), "start@host.com");
    EXPECT_NE(msg.str().find("start@host.com"), std::string::npos);
    Message msg2;
    msg2.set_fromaddr(std::make_pair("Other", "other@domain.com"));
    EXPECT_NE(msg2.str().find("<other@domain.com>"), std::string::npos);
}

TEST_F(PublicMessageTestCase, TestCCDifferent) {
    Message msg("","one@test.com","two@test.com","","cc2@cool.com");
    EXPECT_NE(msg.str().find("cc2@cool.com"), std::string::npos);
}

TEST_F(PublicMessageTestCase, TestBCCDifferent) {
    Message msg("","one2@test.com","two2@test.com","","","secret2@test.com");
    EXPECT_EQ(msg.str().find("secret2@test.com"), std::string::npos); // not found
}

TEST_F(PublicMessageTestCase, TestReplyToDifferent) {
    Message msg("","f1@test.com","f2@test.com","","","", "response@test.com");
    EXPECT_EQ(msg.reply_to(), "response@test.com");
    EXPECT_NE(msg.str().find("response@test.com"), std::string::npos);
}

TEST_F(PublicMessageTestCase, TestProcessAddressDifferent) {
    Message msg;
    msg.set_fromaddr(std::make_pair("X\r\n", "x\r\n@foo.com"));
    msg.set_to({"y\r@foo.com"});
    msg.set_reply_to("z\n@foo.com");
    std::string repr = msg.str();
    EXPECT_NE(repr.find("<x@foo.com>"), std::string::npos);
    EXPECT_NE(repr.find("y@foo.com"), std::string::npos);
    EXPECT_NE(repr.find("z@foo.com"), std::string::npos);
}

TEST_F(PublicMessageTestCase, TestCharsetDifferent) {
    Message msg;
    EXPECT_EQ(msg.charset(), "utf-8");
    Message msg2;
    msg2.set_charset("latin-1");
    EXPECT_EQ(msg2.charset(), "latin-1");
}

TEST_F(PublicMessageTestCase, TestExtraHeadersDifferent) {
    Message msg;
    msg.set_fromaddr("aaa@bbb.com");
    msg.set_to({"ccc@ddd.com"});
    msg.set_extra_headers({{"X-Test-Header-2","AnotherTest"}});
    EXPECT_NE(msg.str().find("X-Test-Header-2: AnotherTest"), std::string::npos);
}

TEST_F(PublicMessageTestCase, TestMailAndRcptOptionsDifferent) {
    Message msg;
    EXPECT_TRUE(msg.mail_options().empty());
    EXPECT_TRUE(msg.rcpt_options().empty());
    Message msg2;
    msg2.set_mail_options({"SOME_SPECIAL=ENABLED"});
    EXPECT_EQ(msg2.mail_options(), std::vector<std::string>{"SOME_SPECIAL=ENABLED"});
    Message msg3;
    msg3.set_rcpt_options({"INFO=YES"});
    EXPECT_EQ(msg3.rcpt_options(), std::vector<std::string>{"INFO=YES"});
}

TEST_F(PublicMessageTestCase, TestToAddrsDifferent) {
    Message msg;
    msg.set_to({"solo@place.net"});
    EXPECT_EQ(msg.to_addrs(), std::set<std::string>{"solo@place.net"});
    Message msg2;
    msg2.set_to({"to@abc.com"});
    msg2.set_cc("xyz@def.com");
    msg2.set_bcc({"hidden@abc.com", "hidden2@abc.com"});
    std::set<std::string> expected = {"to@abc.com", "xyz@def.com", "hidden@abc.com", "hidden2@abc.com"};
    EXPECT_EQ(msg2.to_addrs(), expected);
    Message msg3;
    msg3.set_to({"unique@x.com"});
    msg3.set_cc("unique@x.com");
    EXPECT_EQ(msg3.to_addrs(), std::set<std::string>{"unique@x.com"});
}

TEST_F(PublicMessageTestCase, TestValidateDifferent) {
    Message msg;
    msg.set_fromaddr("onlyfrom@fail.com");
    EXPECT_THROW(msg.validate(), SenderError);
    Message msg2;
    msg2.set_to({"onlyto@fail.com"});
    EXPECT_THROW(msg2.validate(), SenderError);
    Message msg3("bad\r","from@bad.com","to@bad.com");
    EXPECT_THROW(msg3.validate(), SenderError);
    Message msg4("bad\n","from@bad.com","to@bad.com");
    EXPECT_THROW(msg4.validate(), SenderError);
}

TEST_F(PublicMessageTestCase, TestAttachDifferent) {
    Message msg;
    Attachment att("public.txt");
    std::vector<Attachment> atts = {Attachment("a1.pdf"), Attachment("b2.pdf")};
    msg.attach(att);
    EXPECT_EQ(msg.attachments(), std::vector<Attachment>{att});
    msg.attach(atts);
    std::vector<Attachment> expect = {att, atts[0], atts[1]};
    EXPECT_EQ(msg.attachments(), expect);
}

TEST_F(PublicMessageTestCase, TestAttachAttachmentDifferent) {
    Message msg;
    msg.attach_attachment("data.csv", "application/csv", "header1,header2\n1,2");
    EXPECT_EQ(msg.attachments()[0].filename(), "data.csv");
    EXPECT_EQ(msg.attachments()[0].content_type(), "application/csv");
    EXPECT_EQ(msg.attachments()[0].data(), "header1,header2\n1,2");
}

TEST_F(PublicMessageTestCase, TestPlainTextDifferent) {
    std::string plain_text = "Greetings!\nThis is a public test.";
    Message msg;
    msg.set_fromaddr("person@host.com");
    msg.set_to({"person2@host.com"});
    msg.set_body(plain_text);
    EXPECT_EQ(msg.body(), plain_text);
    EXPECT_NE(msg.body().find("Greetings!"), std::string::npos);
    EXPECT_NE(msg.str().find(plain_text), std::string::npos);
}