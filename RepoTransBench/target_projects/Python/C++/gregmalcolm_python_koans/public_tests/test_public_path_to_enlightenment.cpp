#include "gtest/gtest.h"
#include "lib/path_to_enlightenment.h"

TEST(TestPublicPathToEnlightenment, PublicModuleExists) {
    EXPECT_EQ(get_path_to_enlightenment_name(), "runner.path_to_enlightenment");
}

TEST(TestPublicPathToEnlightenment, PublicModuleHasAnyAttribute) {
    auto attrs = get_path_to_enlightenment_attrs();
    bool found = false;
    for (const auto& a : attrs) {
        if (!a.empty() && a[0] != '_') {
            found = true;
            break;
        }
    }
    EXPECT_TRUE(found);
}