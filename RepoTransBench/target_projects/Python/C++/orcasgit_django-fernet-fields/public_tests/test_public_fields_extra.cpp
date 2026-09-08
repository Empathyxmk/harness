#include <gtest/gtest.h>
#include "fields.h"
#include <vector>

// Helper for parameterized test
class FernetFieldPublicParamTest : public ::testing::TestWithParam<std::vector<uint8_t>> {};

TEST(FernetFieldPublicTest, EncryptDecrypt) {
    FernetField field;
    std::vector<uint8_t> data({'S','e','n','s','i','t','i','v','e','P','u','b','l','i','c','D','a','t','a','1','2','3'});
    auto encrypted = field.get_prep_value(data);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, data);
}

TEST(FernetFieldPublicTest, DifferentData) {
    FernetField field;
    std::vector<uint8_t> value({'U','n','i','q','u','e','B','y','t','e','s','F','o','r','P','u','b','l','i','c','T','e','s','t'});
    auto encrypted = field.get_prep_value(value);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, value);
}

TEST(FernetFieldPublicTest, HandlesEmptyBytes) {
    FernetField field;
    std::vector<uint8_t> value;
    auto encrypted = field.get_prep_value(value);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, std::vector<uint8_t>());
}

INSTANTIATE_TEST_SUITE_P(PublicParams, FernetFieldPublicParamTest,
    ::testing::Values(
        std::vector<uint8_t>({'p','u','b','l','i','c','_','p','a','r','a','m','_','1'}),
        std::vector<uint8_t>({'a','n','o','t','h','e','r','_','p','a','r','a','m','_','p','u','b','l','i','c','_','2'}),
        std::vector<uint8_t>({'e','x','t','r','a','_','d','a','t','a','_','p','u','b','l','i','c','_','3'})
    ));

TEST_P(FernetFieldPublicParamTest, FernetFieldParametrize) {
    std::vector<uint8_t> val = GetParam();
    FernetField field;
    auto encrypted = field.get_prep_value(val);
    auto decrypted = field.from_db_value(encrypted);
    EXPECT_EQ(decrypted, val);
}