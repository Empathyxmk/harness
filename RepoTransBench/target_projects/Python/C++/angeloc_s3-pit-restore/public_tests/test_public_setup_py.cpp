#include <gtest/gtest.h>
#include "../src/dummy_setup_py.h"

// Simulate the public import/patch logic for setup.py, testing public fields
TEST(TestPublicSetupPy, CanImportAndCallsSetupPublic) {
    SetupPyModule mod;
    // Patch: simulate call with author fields
    std::map<std::string, std::string> args = {
        {"author", "Angelo Compagnucci"},
        {"author_email", "angelo.compagnucci@gmail.com"},
        {"keywords", "public"}
    };
    mod.setup(args);

    EXPECT_EQ(mod.called["author"], "Angelo Compagnucci");
    EXPECT_EQ(mod.called["author_email"], "angelo.compagnucci@gmail.com");
    EXPECT_TRUE(mod.called_keys.count("keywords") > 0);
}