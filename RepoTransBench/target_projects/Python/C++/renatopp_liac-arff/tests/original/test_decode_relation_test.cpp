#include <gtest/gtest.h>
#include <string>
#include "arff_cpp.h"

class DecodeRelationTest : public ::testing::Test {
protected:
    std::unique_ptr<ArffDecoder> decoder;
    void SetUp() override { decoder = std::make_unique<ArffDecoder>(); }
};

TEST_F(DecodeRelationTest, test_simple) {
    std::string fixture = "@RELATION relation-name";
    EXPECT_EQ(decoder->_decode_relation(fixture), "relation-name");
}
TEST_F(DecodeRelationTest, test_padding) {
    std::string fixture = "@RELATION     relation-name";
    EXPECT_EQ(decoder->_decode_relation(fixture), "relation-name");
}
// ... [CUT: Complete all tests for quotes, spaces and error-expecting with EXPECT_THROW]