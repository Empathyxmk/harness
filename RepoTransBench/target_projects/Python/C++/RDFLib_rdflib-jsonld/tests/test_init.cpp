#include <gtest/gtest.h>
#include "module.h"

TEST(InitTest, ImportModuleBasics) {
    // Check that basic "attributes" exist in namespace
    EXPECT_FALSE(rdflib_jsonld::__doc__.empty());
    EXPECT_FALSE(rdflib_jsonld::__version__.empty());
    EXPECT_FALSE(rdflib_jsonld::__author__.empty());
    EXPECT_FALSE(rdflib_jsonld::__contact__.empty());
    EXPECT_FALSE(rdflib_jsonld::__docformat__.empty());
}