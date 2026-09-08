#include <gtest/gtest.h>
#include <string>
#include "arff_cpp.h"

class EncodeRelationTest : public ::testing::Test {
protected:
    std::unique_ptr<ArffEncoder> encoder;
    void SetUp() override { encoder = std::make_unique<ArffEncoder>(); }
};

TEST_F(EncodeRelationTest, test_simple) {
    EXPECT_EQ(encoder->_encode_relation("relation-name"), "@RELATION relation-name");
}
TEST_F(EncodeRelationTest, test_espaced) {
    EXPECT_EQ(encoder->_encode_relation("relation name and"), "@RELATION \"relation name and\"");
}
TEST_F(EncodeRelationTest, test_special) {
    EXPECT_EQ(encoder->_encode_relation("%relationnameand"), "@RELATION \"%relationnameand\"");
    EXPECT_EQ(encoder->_encode_relation("relation,nameand"), "@RELATION \"relation,nameand\"");
}