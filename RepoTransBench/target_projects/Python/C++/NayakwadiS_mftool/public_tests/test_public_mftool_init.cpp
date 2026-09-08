#include <gtest/gtest.h>
#include <string>
#include <algorithm>

TEST(TestMFInitMinimalPublic, test_dummy_value_public) {
    std::string s = "DUMMY";
    bool all_lower = std::all_of(s.begin(), s.end(), ::islower);
    EXPECT_FALSE(all_lower);
}