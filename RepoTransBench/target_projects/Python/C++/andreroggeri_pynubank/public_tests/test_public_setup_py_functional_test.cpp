#include <gtest/gtest.h>
#include "pynubank/setup_py.h"

TEST(PublicSetupPyFunctionalTest, VersionStringPresent) {
    SetupPy setupPy;
    std::ostringstream out;
    setupPy.printVersion(out);
    EXPECT_FALSE(out.str().empty());
}