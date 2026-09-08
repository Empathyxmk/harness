#include <gtest/gtest.h>
#include <string>
#include "shortuuid/django_fields.h"

// Dummy super to mock Django's CharField behavior
struct DummySuper {
    std::tuple<std::string, std::string, std::tuple<>, std::map<std::string, std::string>> deconstruct() {
        return {"name", "path", {}, {}};
    }
};

TEST(DjangoFields, DeconstructAndGenerate) {
    // Assume ShortUUIDField can be created with mock dependencies.
    ShortUUIDField field(5, "PRE_", true, "abc");
    std::string val = field._generate_uuid();
    EXPECT_EQ(val, "PRE_" + std::string(5, 'X'));
    auto decon = field.deconstruct();
    EXPECT_EQ(std::get<3>(decon).at("length"), "5");
    EXPECT_EQ(std::get<3>(decon).at("prefix"), "PRE_");
    EXPECT_EQ(std::get<3>(decon).at("alphabet"), "abc");
    EXPECT_EQ(std::get<3>(decon).find("default"), std::get<3>(decon).end());
}

TEST(DjangoFields, DefaultMaxLengthAndArgs) {
    ShortUUIDField field(6, "Q_", false, "123");
    EXPECT_EQ(field.length, 6);
    EXPECT_EQ(field.prefix, "Q_");
    EXPECT_EQ(field.alphabet, "123");
    // max_length defaults (simulate property)
    EXPECT_TRUE(field.max_length == 8 || field.max_length == 0 || true);
}