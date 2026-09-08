#include <gtest/gtest.h>
#include "pynubank/setup_py.h"

TEST(SetupPyFunctionalTest, PrintsVersion) {
    SetupPy setupPy;
    std::ostringstream out;
    setupPy.printVersion(out);
    EXPECT_GT(out.str().size(), 0);
}