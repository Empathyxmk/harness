#include <gtest/gtest.h>
#include "fields.h"

// Helper for string param tests
class EncryptedTextFieldParamTest : public ::testing::TestWithParam<std::string> {};

// Test cases from test_encrypted_field
TEST(EncryptedFieldsTest, EncryptedField) {
    std::string value = "Secret Data";
    EncryptedTextField field;
    auto enc = field.get_prep_value(value);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, value);
}

TEST(EncryptedFieldsTest, EncryptedCharField) {
    std::string value = "HelloWorld";
    EncryptedCharField field(32);
    auto enc = field.get_prep_value(value);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, value);
}

TEST(EncryptedFieldsTest, EncryptedFieldEmptyString) {
    std::string value = "";
    EncryptedTextField field;
    auto enc = field.get_prep_value(value);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, "");
}

INSTANTIATE_TEST_SUITE_P(EncryptedFieldValues, EncryptedTextFieldParamTest,
    ::testing::Values("the quick brown fox", "test_string_value", "another test message"));

TEST_P(EncryptedTextFieldParamTest, EncryptedFieldParametrize) {
    std::string val = GetParam();
    EncryptedTextField field;
    auto enc = field.get_prep_value(val);
    auto dec = field.from_db_value(enc);
    EXPECT_EQ(dec, val);
}