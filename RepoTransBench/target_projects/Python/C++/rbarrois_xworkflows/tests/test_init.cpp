#include <gtest/gtest.h>
#include <string>
#include "xworkflows/base.h"
#include "xworkflows/compat.h"

TEST(InitTest, VersionAndBaseImport) {
    // Normal import: __version__ string available and base has Workflow
    std::string version = xworkflows::base::__version__;
    ASSERT_FALSE(version.empty());
    // Check base::Workflow exists as type
    EXPECT_TRUE(xworkflows::base::has_workflow_marker());
}

// For C++, simulating importlib/pkg_resources fallback doesn't apply directly but we simulate logic.
TEST(InitTest, ImportInitFallbackPkgResources) {
    // Simulate dummy version provision, treat similar to Python branch fallback
    std::string version;
    bool fallback_used = false;

    // Simulate 'missing importlib.metadata', uses dummy version, fallback for test
    // In actual C++ code, version might be compiled in or set in a header
    version = xworkflows::base::__version__;
    if (version == "123.45") fallback_used = true;
    // Accept either dummy or normal version, just check string present.
    ASSERT_FALSE(version.empty());
    EXPECT_TRUE(xworkflows::base::has_workflow_marker());
}

// Simulate fallback to hardcoded version if 'both' dynamic sources fail.
TEST(InitTest, FallbackErrorHandling) {
    // In C++: just check fallback constant present, as dynamic import simulation not relevant
    EXPECT_EQ(xworkflows::base::__version__, "1.1.1.dev0");
    EXPECT_TRUE(xworkflows::base::has_workflow_marker());
}