#include <gtest/gtest.h>
#include <string>
#include "linkedin2username.h"

TEST(PublicImportPython, BasicImports) {
    // Simulate dynamic import: just check the type exists
    NameMutator nm("Test Name");
    ASSERT_TRUE(typeid(nm) == typeid(NameMutator));
}