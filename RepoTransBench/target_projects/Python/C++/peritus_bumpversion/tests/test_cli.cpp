#include <gtest/gtest.h>

// This test is skipped because it needs system VCS (hg) setup
TEST(CliTest, SkippedCliTest) {
    GTEST_SKIP() << "requires 'hg' executable and real VCS setup, skipping in CI";
}