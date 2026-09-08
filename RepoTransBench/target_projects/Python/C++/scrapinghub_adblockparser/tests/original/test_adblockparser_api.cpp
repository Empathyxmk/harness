#include <gtest/gtest.h>
#include "adblockparser.h"

// This test simply checks if the key API symbols are available
// In C++ we do not have `hasattr`; so compilation/linking demonstrates presence.

TEST(AdblockparserApiTest, ImportsAvailable) {
    // Try compiling under the assumption that the public API types exist
    // Types must exist for this to compile
    AdblockRules* rules = nullptr;
    AdblockRule* rule = nullptr;
    AdblockParsingError* err = nullptr;
    (void)rules;
    (void)rule;
    (void)err;
    SUCCEED();
}