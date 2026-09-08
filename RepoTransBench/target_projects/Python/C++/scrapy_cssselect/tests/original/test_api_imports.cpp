#include <gtest/gtest.h>
#include "../../src/dummy_cssselect.h"

TEST(TestApiImports, ImportAllAttrs) {
    for (const auto& attr : {
             "ExpressionError",
             "FunctionalPseudoElement",
             "GenericTranslator",
             "HTMLTranslator",
             "Selector",
             "SelectorError",
             "SelectorSyntaxError",
             "parse",
         }) {
        EXPECT_TRUE(cssselect::hasattr(attr));
    }
}

TEST(TestApiImports, Version) {
    EXPECT_TRUE(!cssselect::VERSION.empty());
    EXPECT_EQ(cssselect::VERSION, cssselect::__version__);
}