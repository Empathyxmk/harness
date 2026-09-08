#include <gtest/gtest.h>
#include <filesystem>

TEST(TestPublicDemoScript, demo_png_exists) {
    std::filesystem::path png = std::filesystem::current_path() / "demo" / "demo_01.png";
    EXPECT_TRUE(std::filesystem::exists(png));
}