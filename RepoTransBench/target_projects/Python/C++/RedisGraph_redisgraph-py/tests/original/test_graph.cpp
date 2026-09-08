#include <gtest/gtest.h>

using namespace redisgraph;

class TestGraph : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}
};

// Intentionally left blank as in the original python test (just pass)
TEST_F(TestGraph, Empty) {}