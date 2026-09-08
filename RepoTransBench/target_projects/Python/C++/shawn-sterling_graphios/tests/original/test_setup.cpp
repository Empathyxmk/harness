#include <gtest/gtest.h>
#include <fstream>
#include <string>

TEST(SetupPy, Importable) {
    std::ifstream ifs("setup.py");
    EXPECT_TRUE(ifs.good());
}

TEST(SetupPy, DISABLED_MainFunctionality) {
    // Not suitable for direct loading; skip like pytest.mark.skip
    SUCCEED();
}