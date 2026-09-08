#include <gtest/gtest.h>
#include <string>
#include <set>
#include <map>
#include <optional>

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
        std::optional<Config> config = std::nullopt,
        std::optional<std::set<std::string>> expand_functions_ = std::nullopt,
        std::optional<std::map<std::string, std::string>> identifiers_ = std::nullopt,
        std::optional<std::set<std::string>> prefixes_ = std::nullopt,
        std::optional<bool> reduce_assignments_ = std::nullopt,
        std::optional<bool> use_math_symbols_ = std::nullopt,
        std::optional<bool> use_set_symbols_ = std::nullopt,
        std::optional<bool> use_signature_ = std::nullopt,
        std::optional<bool> escape_underscores_ = std::nullopt
    ) const {
        Config c;
        if (config) c = *config;
        else c = *this;
        if (expand_functions_) c.expand_functions = *expand_functions_;
        if (identifiers_) c.identifiers = *identifiers_;
        if (prefixes_) c.prefixes = *prefixes_;
        if (reduce_assignments_) c.reduce_assignments = *reduce_assignments_;
        if (use_math_symbols_) c.use_math_symbols = *use_math_symbols_;
        if (use_set_symbols_) c.use_set_symbols = *use_set_symbols_;
        if (use_signature_) c.use_signature = *use_signature_;
        if (escape_underscores_) c.escape_underscores = *escape_underscores_;
        return c;
    }
};

TEST(PublicConfig, MergeAndDefaultsPublic) {
    Config c = Config::defaults();
    Config merged = c.merge(std::nullopt, std::nullopt, std::nullopt, std::nullopt, true);
    EXPECT_TRUE(merged.reduce_assignments);
    EXPECT_FALSE(merged.use_math_symbols);
    EXPECT_TRUE(merged.expand_functions.empty());

    Config c2 = Config::defaults().merge(std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, true, false);
    Config merged2 = c.merge(c2, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, true);
    EXPECT_TRUE(merged2.use_set_symbols);
    EXPECT_TRUE(merged2.use_signature);
    EXPECT_TRUE(merged2.escape_underscores);

    Config merged3 = c.merge(std::nullopt, std::nullopt, std::map<std::string,std::string>{{"z","omega"}});
    EXPECT_EQ(merged3.identifiers.size(), 1);
    EXPECT_TRUE(merged3.expand_functions.empty());

    Config conf_a = c.merge(std::nullopt, std::nullopt, std::nullopt, std::set<std::string>{"prefix"}).merge(std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, false);
    Config conf_b = Config::defaults().merge(std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt, true);
    Config result = conf_a.merge(conf_b);
    EXPECT_TRUE(result.use_signature);
    EXPECT_TRUE(result.use_set_symbols);
}

TEST(PublicConfig, ConfigDefaultsPublic) {
    Config defaults = Config::defaults();
    EXPECT_TRUE(defaults.expand_functions.empty());
    EXPECT_TRUE(defaults.identifiers.empty());
    EXPECT_TRUE(defaults.prefixes.empty());
    EXPECT_FALSE(defaults.reduce_assignments);
    EXPECT_FALSE(defaults.use_math_symbols);
    EXPECT_FALSE(defaults.use_set_symbols);
    EXPECT_TRUE(defaults.use_signature);
    EXPECT_TRUE(defaults.escape_underscores);
}