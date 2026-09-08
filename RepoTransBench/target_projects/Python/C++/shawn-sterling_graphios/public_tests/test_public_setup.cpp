#include <gtest/gtest.h>
#include <fstream>
#include <string>

TEST(PublicSetup, PyRuns) {
    std::ifstream ifs("../setup.py");
    EXPECT_TRUE(ifs.good());
}