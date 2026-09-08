// Already provided in last batch, but ensuring completeness from htmlcov/test_sender_extended_py.html
#include <gtest/gtest.h>
#include "attachment.h"

class AttachmentTestCase : public ::testing::Test {};

TEST_F(AttachmentTestCase, TestAttachmentCreation) {
    Attachment a("test.txt");
    EXPECT_EQ(a.filename(), "test.txt");
    EXPECT_FALSE(a.filename().empty());
}

TEST_F(AttachmentTestCase, TestAttachmentRepr) {
    Attachment a("test.txt");
    std::string repr = a.repr();
    EXPECT_NE(repr.find("Attachment"), std::string::npos);
}
// No as_mime or empty class block; module can always be safely included