#include <gtest/gtest.h>
#include "attachment.h"

class PublicAttachmentTestCase : public ::testing::Test {};

TEST_F(PublicAttachmentTestCase, TestAttachmentCreationDifferentFile) {
    Attachment a("newfile.pdf");
    EXPECT_EQ(a.filename(), "newfile.pdf");
    EXPECT_FALSE(a.filename().empty());
}

TEST_F(PublicAttachmentTestCase, TestAttachmentReprDifferentFile) {
    Attachment a("readme.md");
    std::string repr = a.repr();
    EXPECT_NE(repr.find("Attachment"), std::string::npos);
}