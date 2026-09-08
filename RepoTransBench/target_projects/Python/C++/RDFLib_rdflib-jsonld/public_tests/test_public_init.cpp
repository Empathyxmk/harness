#include <gtest/gtest.h>
#include "module.h"

TEST(PublicInit, ImportRdflibJsonldPublic) {
    // Test attribute types and existence
    EXPECT_TRUE(typeid(rdflib_jsonld::__doc__).name() == typeid(std::string).name());
    EXPECT_TRUE(typeid(rdflib_jsonld::__version__).name() == typeid(std::string).name());
    EXPECT_TRUE(typeid(rdflib_jsonld::__author__).name() == typeid(std::string).name());
    EXPECT_TRUE(typeid(rdflib_jsonld::__contact__).name() == typeid(std::string).name());
    EXPECT_TRUE(typeid(rdflib_jsonld::__docformat__).name() == typeid(std::string).name());
}