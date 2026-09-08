#include <gtest/gtest.h>
#include <set>
#include <map>
#include <optional>
#include <string>

struct Config {
    std::set<std::string> expand_functions;
    std::map<std::string, std::string> identifiers;
    std::set<std::string> prefixes;
    bool reduce_assignments = false;
    bool use_math_symbols = false;
    bool use_set_symbols = false;
    bool use_signature = true;
    bool escape_underscores = true;

    static Config defaults() { return Config{}; }
    Config merge(
        std::optional<std::set<std::string>> expand_functions_ = std::nullopt,
        std::optional<std::map<std::string, std::string>> identifiers_ = std::nullopt,
        std::optional<std::set<std::string>> prefixes_ = std::nullopt,
        std::optional<bool> reduce_assignments_ = std::nullopt,
        std::optional<bool> use_math_symbols_ = std::nullopt,
        std::optional<bool> use_set_symbols_ = std::nullopt,
        std::optional<bool> use_signature_ = std::nullopt,
        std::optional<bool> escape_underscores_ = std::nullopt,
        std::optional<Config> config = std::nullopt
    ) const {
        Config c = *this;
        if (expand_functions_) c.expand_functions = *expand_functions_;
        if (identifiers_) c.identifiers = *identifiers_;
        if (prefixes_) c.prefixes = *prefixes_;
        if (reduce_assignments_) c.reduce_assignments = *reduce_assignments_;
        if (use_math_symbols_) c.use_math_symbols = *use_math_symbols_;
        if (use_set_symbols_) c.use_set_symbols = *use_set_symbols_;
        if (use_signature_) c.use_signature = *use_signature_;
        if (escape_underscores_) c.escape_underscores = *escape_underscores_;
        if (config) {
            c = *config;
        }
        return c;
    }
};

TEST(PublicConfigExtra, MergeExplicitKeysPublic) {
    Config c = Config::defaults();
    Config merged = c.merge(std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, false, false);
    EXPECT_FALSE(merged.escape_underscores);
    EXPECT_FALSE(merged.use_signature);
    EXPECT_EQ(merged.reduce_assignments, c.reduce_assignments);

    Config m2 = c.merge(std::set<std::string>{"fn"}, std::nullopt, std::set<std::string>{"foo.bar","baz.invalid"});
    EXPECT_EQ(m2.prefixes, (std::set<std::string>{"foo.bar","baz.invalid"}));
    EXPECT_EQ(m2.expand_functions, (std::set<std::string>{"fn"}));

    Config c_other = c.merge(std::nullopt, std::nullopt, std::nullopt, std::nullopt, true);
    Config m3 = c.merge(std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, c_other);
    EXPECT_TRUE(m3.use_math_symbols);
    EXPECT_EQ(m3.reduce_assignments, c.reduce_assignments);
    EXPECT_TRUE(m3.escape_underscores);
}