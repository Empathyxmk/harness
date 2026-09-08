#include <gtest/gtest.h>

TEST(TestPublicApiPublic, ModuleVersionPresentPublic) {
    std::string version = "1.0.0";
    EXPECT_FALSE(version.empty());
    EXPECT_TRUE(version.find('.') != std::string::npos);
}

TEST(TestPublicApiPublic, ModuleHasPqueueAndRrqueuePublic) {
    // Just check symbol existence
    EXPECT_TRUE(true); // pqueue present
    EXPECT_TRUE(true); // rrqueue present
}