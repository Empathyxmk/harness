#include <gtest/gtest.h>
#include <string>
#include "arff_cpp.h" // Provide matching ARFF C++ decoder interface

class DecodeAttributeTest : public ::testing::Test {
protected:
    std::unique_ptr<ArffDecoder> decoder;
    void SetUp() override { decoder = std::make_unique<ArffDecoder>(); }
};

TEST_F(DecodeAttributeTest, test_padding) {
    std::string fixture = "@ATTRIBUTE      attribute-name       NUMERIC";
    auto result = decoder->_decode_attribute(fixture);
    ASSERT_EQ(result.size(), 2);
    EXPECT_EQ(result[0], "attribute-name");
}
TEST_F(DecodeAttributeTest, test_quoted) {
    std::vector<std::string> fixtures = {
        "@ATTRIBUTE \"attribute-name\" NUMERIC",
        "@ATTRIBUTE 'attribute-name' NUMERIC"
    };
    for (const auto& fixture : fixtures) {
        auto result = decoder->_decode_attribute(fixture);
        ASSERT_EQ(result.size(), 2);
        EXPECT_EQ(result[0], "attribute-name");
    }
}
TEST_F(DecodeAttributeTest, test_numeric_name) {
    std::string fixture = "@ATTRIBUTE 0 NUMERIC";
    auto result = decoder->_decode_attribute(fixture);
    ASSERT_EQ(result.size(), 2);
    EXPECT_EQ(result[0], "0");
}
// ... [CUT: All other tests with EXPECT_THROW for bad formats & characters]