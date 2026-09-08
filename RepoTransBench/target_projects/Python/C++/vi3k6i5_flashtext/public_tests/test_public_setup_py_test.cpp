#include <gtest/gtest.h>
#include <string>
#include <cstdio>

TEST(PublicSetupPy, SetupPyPresent) {
    FILE* f = fopen("setup.py", "r");
    ASSERT_TRUE(f != nullptr);
    if (f) fclose(f);
}