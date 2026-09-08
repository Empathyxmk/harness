#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "arff_cpp.h"

class EncodeTest : public ::testing::Test {
protected:
    std::unique_ptr<ArffEncoder> encoder;
    void SetUp() override { encoder = std::make_unique<ArffEncoder>(); }
};

TEST_F(EncodeTest, test_encode) {
    ARFFObject obj = ...; // Fill from OBJ C++ equivalent
    std::string expected = ...; // Fill from ARFF string literal
    EXPECT_EQ(encoder->encode(obj), expected);
}
// ... [CUT: Implement all object validity, parsing, string encoding, and edge/assertion cases from Python]