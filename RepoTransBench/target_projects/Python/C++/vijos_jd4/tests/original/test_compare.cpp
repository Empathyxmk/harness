#include <gtest/gtest.h>
#include "jd4/compare.h"
#include <string>
#include <vector>

TEST(CompareTest, Small)
{
    EXPECT_TRUE(compare_stream("", ""));
    EXPECT_TRUE(compare_stream("a", "a"));
    EXPECT_FALSE(compare_stream("a", "b"));
    EXPECT_TRUE(compare_stream("bar", "bar"));
    EXPECT_FALSE(compare_stream("bar", "baz"));
    EXPECT_FALSE(compare_stream("bar", "baz"));
}

TEST(CompareTest, APlusB)
{
    std::string answer = "1 2\r\n";
    std::vector<std::string> trues = {
        "1 2", "1 2\n", "1 2\r", "1 2\r\n", "1 2 ", "1 2 \n", "1 2 \r", "1 2 \r\n",
        "1  2", "1  2\n", "1  2\r", "1  2\r\n", "1  2 ", "1  2 \n", "1  2 \r", "1  2 \r\n",
        " 1 2", " 1 2\n", " 1 2\r", " 1 2\r\n", " 1 2 ", " 1 2 \n", " 1 2 \r", " 1 2 \r\n"
    };
    for (const auto& s : trues)
        EXPECT_TRUE(compare_stream(answer, s));

    std::vector<std::string> falses = {
        "1 1", "1 1\n", "1 1\r", "1 1\r\n", "1 1 ", "1 1 \n", "1 1 \r", "1 1 \r\n",
        " 1 1", " 1 1\n", " 1 1\r", " 1 1\r\n", " 1 1 ", " 1 1 \n", " 1 1 \r", " 1 1 \r\n",
        "2 2", "2 2\n", "2 2\r", "2 2\r\n", "2 2 ", "2 2 \n", "2 2 \r", "2 2 \r\n",
        " 2 2", " 2 2\n", " 2 2\r", " 2 2\r\n", " 2 2 ", " 2 2 \n", " 2 2 \r", " 2 2 \r\n",
        "2 1", "2 1\n", "2 1\r", "2 1\r\n", "2 1 ", "2 1 \n", "2 1 \r", "2 1 \r\n",
        " 2 1", " 2 1\n", " 2 1\r", " 2 1\r\n", " 2 1 ", " 2 1 \n", " 2 1 \r", " 2 1 \r\n",
        "12"
    };
    for (const auto& s : falses)
        EXPECT_FALSE(compare_stream(answer, s));
}

TEST(CompareTest, Large)
{
    std::string a(1048576, 'a');
    EXPECT_TRUE(compare_stream(a, a));
    std::string b = a.substr(0, 1048575) + "b";
    EXPECT_FALSE(compare_stream(a, b));
    std::string d = a + " " + std::string(1048576, 'b') + "\r\n";
    std::string e = a + std::string(1048576, ' ') + std::string(1048576, 'b');
    EXPECT_TRUE(compare_stream(d, e));
}