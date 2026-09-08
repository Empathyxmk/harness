#include <gtest/gtest.h>
#include "jd4/case.h"
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <filesystem>

namespace fs = std::filesystem;

TEST(CaseTest, LegacyCase)
{
    fs::path cur_dir = fs::path(__FILE__).parent_path();
    fs::path datafile = cur_dir / "testdata" / "aplusb-legacy.zip";
    std::ifstream file(datafile, std::ios::binary);
    ASSERT_TRUE(file.is_open());

    std::vector<Case> cases = read_cases(file);
    int count = 0;
    for (const auto& c : cases) {
        EXPECT_EQ(c.time_limit_ns, 1000000000);
        EXPECT_EQ(c.memory_limit_bytes, 16777216);
        EXPECT_EQ(c.score, 10);

        std::istringstream in(c.input);
        std::istringstream out(c.output);
        int a, b;
        in >> a >> b;
        int expected;
        out >> expected;
        EXPECT_EQ(a + b, expected);
        count += 1;
    }
    EXPECT_EQ(count, 10);
}

TEST(CaseTest, YamlCase)
{
    fs::path cur_dir = fs::path(__FILE__).parent_path();
    fs::path datafile = cur_dir / "testdata" / "aplusb.zip";
    std::ifstream file(datafile, std::ios::binary);
    ASSERT_TRUE(file.is_open());

    std::vector<Case> cases = read_cases(file);
    int count = 0;
    for (const auto& c : cases) {
        EXPECT_EQ(c.time_limit_ns, 1000000000);
        EXPECT_EQ(c.memory_limit_bytes, 33554432);
        EXPECT_EQ(c.score, 10);

        std::istringstream in(c.input);
        std::istringstream out(c.output);
        int a, b;
        in >> a >> b;
        int expected;
        out >> expected;
        EXPECT_EQ(a + b, expected);
        count += 1;
    }
    EXPECT_EQ(count, 10);
}