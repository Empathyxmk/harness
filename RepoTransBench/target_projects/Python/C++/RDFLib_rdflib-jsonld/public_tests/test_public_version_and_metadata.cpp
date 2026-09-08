#include <gtest/gtest.h>
#include "module.h"
#include <fstream>
#include <string>
#include <algorithm>

using namespace rdflib_jsonld;

std::string getSetupPyPath() {
    // Assume setup.py in project root
    return std::string("setup.py");
}

TEST(PublicVersionMeta, ModuleHasVersion) {
    ASSERT_FALSE(__version__.empty());
    int dot_count = std::count(__version__.begin(), __version__.end(), '.');
    EXPECT_GE(dot_count, 1);
}

TEST(PublicVersionMeta, ModuleAuthorAndContact) {
    ASSERT_FALSE(__author__.empty());
    ASSERT_FALSE(__contact__.empty());

    EXPECT_TRUE(__contact__.find("@") != std::string::npos);
    EXPECT_TRUE(__contact__.find(".") != std::string::npos);
}

TEST(PublicVersionMeta, SetupPyHasImportOrClass) {
    std::ifstream ifs(getSetupPyPath());
    ASSERT_TRUE(ifs.good()) << "setup.py not found";
    std::string contents((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
    std::string lowered = contents;
    std::transform(lowered.begin(), lowered.end(), lowered.begin(), ::tolower);
    EXPECT_TRUE(lowered.find("import") != std::string::npos || lowered.find("class") != std::string::npos);
}

TEST(PublicVersionMeta, ModuleDocstringMentionsJSONLD) {
    ASSERT_FALSE(__doc__.empty());
    std::string doc_lower = __doc__;
    std::transform(doc_lower.begin(), doc_lower.end(), doc_lower.begin(), ::tolower);
    EXPECT_TRUE(doc_lower.find("jsonld") != std::string::npos || doc_lower.find("json-ld") != std::string::npos);
}