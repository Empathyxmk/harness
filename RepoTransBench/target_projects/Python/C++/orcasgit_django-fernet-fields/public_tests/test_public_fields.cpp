#include <gtest/gtest.h>
#include "fields.h"

// Helper for parameterized test
class EncryptedTextFieldPublicParamTest : public ::testing::TestWithParam<std::string> {};

TEST(PublicFieldsTest, EncryptedFieldBasic) {
    std::string value = "This is secret data for pub";
    EncryptedTextField field;
    auto enc = field.get_prep_value(value);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, value);
}

TEST(PublicFieldsTest, EncryptedCharField) {
    std::string value = "AlphaBravo";
    EncryptedCharField field(32);
    auto enc = field.get_prep_value(value);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, value);
}

TEST(PublicFieldsTest, EncryptedFieldEmptyString) {
    std::string value = "";
    EncryptedTextField field;
    auto enc = field.get_prep_value(value);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, "");
}

INSTANTIATE_TEST_SUITE_P(PublicFieldParamTest, EncryptedTextFieldPublicParamTest,
    ::testing::Values("fox jumps over the lazy dog",
                      "crazy_test_value_PUBLIC_CASE",
                      "another secret message")
);
TEST_P(EncryptedTextFieldPublicParamTest, EncryptedFieldParametrize) {
    std::string val = GetParam();
    EncryptedTextField field;
    auto enc = field.get_prep_value(val);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, val);
}