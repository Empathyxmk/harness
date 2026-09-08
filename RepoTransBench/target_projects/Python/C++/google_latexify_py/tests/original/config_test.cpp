#include <gtest/gtest.h>
#include <string>
#include <set>
#include <map>
#include <memory>

struct Config {
    std::set<std::string> expand_functions;
    std::map<std::string, std::string> identifiers;
    std::set<std::string> prefixes;
    bool reduce_assignments = false;
    bool use_math_symbols = false;
    bool use_set_symbols = false;
    bool use_signature = true;
    bool escape_underscores = true;

    static Config defaults() {
        return Config{};
    }
    Config merge(
        std::set<std::string> expand_functions_ = {},
        std::map<std::string, std::string> identifiers_ = {},
        std::set<std::string> prefixes_ = {},
        std::optional<bool> reduce_assignments_ = std::nullopt,
        std::optional<bool> use_math_symbols_ = std::nullopt,
        std::optional<bool> use_set_symbols_ = std::nullopt,
        std::optional<bool> use_signature_ = std::nullopt,
        std::optional<bool> escape_underscores_ = std::nullopt
    ) const {
        Config c = *this;
        if (!expand_functions_.empty()) c.expand_functions = expand_functions_;
        if (!identifiers_.empty()) c.identifiers = identifiers_;
        if (!prefixes_.empty()) c.prefixes = prefixes_;
        if (reduce_assignments_.has_value()) c.reduce_assignments = reduce_assignments_.value();
        if (use_math_symbols_.has_value()) c.use_math_symbols = use_math_symbols_.value();
        if (use_set_symbols_.has_value()) c.use_set_symbols = use_set_symbols_.value();
        if (use_signature_.has_value()) c.use_signature = use_signature_.value();
        if (escape_underscores_.has_value()) c.escape_underscores = escape_underscores_.value();
        return c;
    }
    std::string to_string() const {
        return "expand_functions=" + std::to_string(expand_functions.size());
    }
};
TEST(ConfigTest, MergeFieldPrecedenceAndTypes) {
    Config c = Config::defaults().merge(
        {"f"}, {{"a","b"}}, {"p."}, true, true, true, false, false
    );
    Config merged = c.merge();
    EXPECT_EQ(merged.expand_functions, c.expand_functions);
}
TEST(ConfigTest, StrAndRepr) {
    Config conf = Config::defaults();
    std::string s = conf.to_string();
    EXPECT_NE(s.find("expand_functions"), std::string::npos);
}
TEST(ConfigTest, DefaultsIsAConfig) {
    Config c = Config::defaults();
    (void)c;
}
TEST(ConfigTest, MergeDifferentTypes) {
    Config c1 = Config::defaults();
    Config c2 = c1.merge({}, {}, {}, std::nullopt, false);
    EXPECT_FALSE(c2.use_math_symbols);
}