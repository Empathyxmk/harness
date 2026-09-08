#include <gtest/gtest.h>
#include <string>

// Adapted for public test logic
static const std::vector<std::pair<int, std::string>> PUBLIC_CASES = {
    {1, "1"},
    {2, "Foo"},
    {7, "Bar"},
    {14, "FooBar"},
    {8, "Foo"},
    {13, "13"}
};

static std::string foobar(int number) {
    const std::vector<std::pair<int, std::string>> RULES = {
        {2 * 7, "FooBar"},
        {2, "Foo"},
        {7, "Bar"},
    };
    for (const auto& rule : RULES)
        if (number % rule.first == 0)
            return rule.second;
    return std::to_string(number);
}

TEST(PublicParametrize, FoobarCases) {
    for (const auto& x : PUBLIC_CASES) {
        EXPECT_EQ(foobar(x.first), x.second);
    }
}