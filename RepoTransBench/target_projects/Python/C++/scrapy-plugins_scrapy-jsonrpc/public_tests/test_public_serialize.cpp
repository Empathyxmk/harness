#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <tuple>
#include "src/lib/serialize.h"

TEST(PublicSerializeTest, PublicJsonDumpsAndLoads) {
    nlohmann::json orig = {{"c", 100}, {"test", std::vector<int>{1,7,8}}};
    std::string encoded = json_dumps(orig);
    auto decoded = json_loads(encoded);
    EXPECT_EQ(decoded, orig);
}

TEST(PublicSerializeTest, PublicReprLoadsAndDumps) {
    auto orig = std::make_tuple(11, nlohmann::json({{"foo", "bar"}}), std::make_tuple(3,4));
    std::string dumped = repr_dumps(orig);
    auto loaded = repr_loads<decltype(orig)>(dumped);
    EXPECT_EQ(loaded, orig);
}

TEST(PublicSerializeTest, PublicReprDumpsHandlesNone) {
    std::optional<int> val = std::nullopt;
    std::string dumped = repr_dumps(val);
    auto loaded = repr_loads<std::optional<int>>(dumped);
    EXPECT_FALSE(loaded.has_value());
}

TEST(PublicSerializeTest, UnicodeAndUtf8) {
    std::string s_unicode = u8"üñîçødê";
    auto utf8ed = to_utf8(s_unicode);
    EXPECT_TRUE(typeid(utf8ed) == typeid(std::vector<uint8_t>));
    EXPECT_EQ(std::string(utf8ed.begin(), utf8ed.end()), s_unicode);

    std::string s_bytes = u8"测试";
    auto s_str = to_unicode(std::vector<uint8_t>(s_bytes.begin(), s_bytes.end()));
    EXPECT_TRUE(typeid(s_str) == typeid(std::string));
    EXPECT_EQ(s_str, "测试");
}