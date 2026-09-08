#include <gtest/gtest.h>
#include <string>
#include <algorithm>

TEST(TestMFInitMinimal, test_dummy_value) {
    std::string s = "dummy";
    // std::islower(ch) for all chars. All should be lower
    bool all_lower = std::all_of(s.begin(), s.end(), ::islower);
    EXPECT_TRUE(all_lower);
}