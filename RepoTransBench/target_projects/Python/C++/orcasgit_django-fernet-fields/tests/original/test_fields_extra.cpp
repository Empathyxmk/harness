#include <gtest/gtest.h>
#include "fields.h"
#include <vector>

// Helper for param tests
class FernetFieldParamTest : public ::testing::TestWithParam<std::vector<uint8_t>> {};

TEST(FernetFieldTest, EncryptDecrypt) {
    FernetField field;
    std::vector<uint8_t> data({'S','e','n','s','i','t','i','v','e','D','a','t','a','1','2','3'});
    auto encrypted = field.get_prep_value(data);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, data);
}

TEST(FernetFieldTest, DifferentData) {
    FernetField field;
    std::vector<uint8_t> value({'A','n','o','t','h','e','r','S','e','c','r','e','t'});
    auto encrypted = field.get_prep_value(value);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, value);
}

TEST(FernetFieldTest, HandlesEmptyBytes) {
    FernetField field;
    std::vector<uint8_t> value;
    auto encrypted = field.get_prep_value(value);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, std::vector<uint8_t>());
}

INSTANTIATE_TEST_SUITE_P(FernetParams, FernetFieldParamTest,
    ::testing::Values(
        std::vector<uint8_t>({'p','a','r','a','m','_','1'}),
        std::vector<uint8_t>({'p','a','r','a','m','_','2'}),
        std::vector<uint8_t>({'p','a','r','a','m','_','3'})
    ));

TEST_P(FernetFieldParamTest, FernetFieldParametrize) {
    std::vector<uint8_t> val = GetParam();
    FernetField field;
    auto encrypted = field.get_prep_value(val);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, val);
}