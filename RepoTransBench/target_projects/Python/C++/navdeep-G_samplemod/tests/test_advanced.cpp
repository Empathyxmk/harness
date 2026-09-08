#include <gtest/gtest.h>
#include "core.h"

// Simulates: assert sample.hmm() is None
// hmm() returns void in C++, just call and make sure no crash
TEST(AdvancedTestSuite, test_thoughts) {
    hmm();
    SUCCEED();
}