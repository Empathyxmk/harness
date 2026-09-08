#include <gtest/gtest.h>
#include <string>
#include "arff_cpp.h"

class EncodeCommentTest : public ::testing::Test {
protected:
    std::unique_ptr<ArffEncoder> encoder;
    void SetUp() override { encoder = std::make_unique<ArffEncoder>(); }
};

TEST_F(EncodeCommentTest, test_simple) {
    EXPECT_EQ(encoder->_encode_comment("This is a simple comment."), "% This is a simple comment.");
}