#include <gtest/gtest.h>
#include "../../src/dummy_setup_py.h"

// Simulate the import and patching logic of setup.py in C++
TEST(TestSetupPy, CanImportAndCallsSetup) {
    SetupPyModule mod;
    // Patch/setup: simulate calling setup with test data matching Python test
    std::map<std::string, std::string> args = {
        {"name", "s3-pit-restore"},
        {"version", "0.9"},
        {"install_requires", "any"}
    };
    mod.setup(args);

    EXPECT_EQ(mod.called["name"], "s3-pit-restore");
    EXPECT_EQ(mod.called["version"], "0.9");
    EXPECT_TRUE(mod.called_keys.count("install_requires") > 0);
}