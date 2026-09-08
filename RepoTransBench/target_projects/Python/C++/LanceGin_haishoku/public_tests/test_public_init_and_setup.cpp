#include <gtest/gtest.h>
#include <filesystem>

TEST(TestPublicInitAndSetup, init_module_exists) {
    EXPECT_TRUE(std::filesystem::exists("include/haishoku/alg.h"));
}

TEST(TestPublicInitAndSetup, alg_module_exists) {
    EXPECT_TRUE(std::filesystem::exists("include/haishoku/alg.h"));
}