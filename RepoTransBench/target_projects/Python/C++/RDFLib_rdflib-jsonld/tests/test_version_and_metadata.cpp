#include <gtest/gtest.h>
#include "module.h"
#include <string>

using namespace rdflib_jsonld;

TEST(VersionAndMetadataTest, VersionDefined) {
    EXPECT_EQ(typeid(__version__).name(), typeid(std::string).name());
    EXPECT_EQ(__version__, "0.6.2");
}

TEST(VersionAndMetadataTest, AuthorDefined) {
    EXPECT_EQ(typeid(__author__).name(), typeid(std::string).name());
    EXPECT_NE(__author__.find("RDFLib"), std::string::npos);
}

TEST(VersionAndMetadataTest, ContactDefined) {
    EXPECT_EQ(typeid(__contact__).name(), typeid(std::string).name());
    EXPECT_NE(__contact__.find("@"), std::string::npos);
}

TEST(VersionAndMetadataTest, DocformatDefined) {
    EXPECT_EQ(typeid(__docformat__).name(), typeid(std::string).name());
    EXPECT_EQ(__docformat__, "restructuredtext");
}

TEST(VersionAndMetadataTest, ModuleDocstringExists) {
    std::string doc = __doc__;
    ASSERT_FALSE(doc.empty());
    std::string low = doc;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    // Check for "plugin for rdflib" or "a plugin for rdflib"
    EXPECT_TRUE(low.find("plugin for rdflib") != std::string::npos ||
                low.find("a plugin for rdflib") != std::string::npos);
}