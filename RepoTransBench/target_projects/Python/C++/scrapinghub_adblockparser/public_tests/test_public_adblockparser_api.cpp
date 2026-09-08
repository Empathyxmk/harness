#include <gtest/gtest.h>
#include "adblockparser.h"

TEST(PublicAdblockparserApiTest, PublicImportsAvailable) {
    // The presence of these types allows compilation; for runtime, we simply succeed.
    AdblockRules* rules = nullptr;
    AdblockRule* rule = nullptr;
    AdblockParsingError* err = nullptr;
    (void)rules;
    (void)rule;
    (void)err;
    SUCCEED();
}