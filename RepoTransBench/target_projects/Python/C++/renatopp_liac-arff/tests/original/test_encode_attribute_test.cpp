#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "arff_cpp.h"

class EncodeAttributeTest : public ::testing::Test {
protected:
    std::unique_ptr<ArffEncoder> encoder;
    void SetUp() override { encoder = std::make_unique<ArffEncoder>(); }
};

TEST_F(EncodeAttributeTest, test_attribute_name) {
    EXPECT_EQ(encoder->_encode_attribute("attribute name", "REAL"), "@ATTRIBUTE \"attribute name\" REAL");
}

// ... [CUT: Implement all other encoding type/nominal/special cases]