#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <string>

TEST(PublicJsonfieldTest, PublicEncodeSimpleDict) {
    nlohmann::json data = {{"planet", "Saturn"}, {"rings", true}};
    std::string encoded = data.dump();
    ASSERT_EQ(encoded, "{\"planet\":\"Saturn\",\"rings\":true}");
}

TEST(PublicJsonfieldTest, PublicEncodeListNumbers) {
    nlohmann::json data = {5, 7, 11};
    std::string encoded = data.dump();
    ASSERT_EQ(encoded, "[5,7,11]");
}

TEST(PublicJsonfieldTest, PublicDecodeUnicode) {
    std::string input_str = "{\"emoji\": \"\\u263A\"}";
    nlohmann::json output = nlohmann::json::parse(input_str);
    ASSERT_EQ(output["emoji"].get<std::string>(), "\u263A");
}

TEST(PublicJsonfieldTest, PublicInvalidJsonRaises) {
    std::string bad_json = "{invalid: true,}";
    ASSERT_THROW(nlohmann::json::parse(bad_json), nlohmann::json::parse_error);
}

TEST(PublicJsonfieldTest, PublicNativeFloatEncoding) {
    double val = 42.42;
    std::string encoded = nlohmann::json(val).dump();
    ASSERT_EQ(encoded, "42.42");
    auto loaded = nlohmann::json::parse("42.42").get<double>();
    ASSERT_EQ(loaded, val);
}