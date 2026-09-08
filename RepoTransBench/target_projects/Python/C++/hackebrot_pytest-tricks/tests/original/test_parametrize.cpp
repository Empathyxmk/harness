#include <gtest/gtest.h>
#include <string>
#include <vector>

struct FizzBuzzCase {
    int number;
    std::string expected;
};

static const std::vector<FizzBuzzCase> fizzbuzz_cases = {
    {1, "1"},
    {3, "Fizz"},
    {5, "Buzz"},
    {10, "Buzz"},
    {15, "FizzBuzz"},
    {16, "16"}
};

static std::string fizzbuzz(int number) {
    const std::vector<std::pair<int, std::string>> RULES = {
        {3 * 5, "FizzBuzz"},
        {3, "Fizz"},
        {5, "Buzz"}
    };
    for (const auto& rule: RULES)
        if (number % rule.first == 0)
            return rule.second;
    return std::to_string(number);
}

class FizzBuzzTest : public ::testing::TestWithParam<FizzBuzzCase> {};

INSTANTIATE_TEST_SUITE_P(Default, FizzBuzzTest, ::testing::ValuesIn(fizzbuzz_cases));

TEST_P(FizzBuzzTest, fizzbuzz) {
    auto param = GetParam();
    EXPECT_EQ(fizzbuzz(param.number), param.expected);
}