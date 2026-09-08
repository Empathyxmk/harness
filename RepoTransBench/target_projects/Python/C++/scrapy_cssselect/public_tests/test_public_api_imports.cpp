#include <gtest/gtest.h>
#include "../src/dummy_cssselect.h"

TEST(TestApiImportsPublic, ImportSomeAttrsPublic) {
    for (const auto& attr : {
             "GenericTranslator",
             "parse",
             "SelectorError",
             "Selector",
             "HTMLTranslator",
         }) {
        EXPECT_TRUE(cssselect::hasattr(attr));
    }
}

TEST(TestApiImportsPublic, VersionPublic) {
    EXPECT_NE(cssselect::VERSION, "");
    EXPECT_TRUE(!cssselect::__version__.empty());
    EXPECT_GT(cssselect::__version__.length(), 0u);
}