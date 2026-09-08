#include <gtest/gtest.h>
#include "xworkflows/base.h"

TEST(PublicInit, VersionAndBaseImportPublic) {
    std::string version = xworkflows::base::__version__;
    EXPECT_FALSE(version.empty());
    EXPECT_TRUE(xworkflows::base::has_workflow_enabled_marker());
}

TEST(PublicInit, ImportInitFallbackPkgResourcesPublic) {
    std::string version = xworkflows::base::__version__;
    EXPECT_FALSE(version.empty());
    // Simulate check for ForbiddenTransition marker
    EXPECT_TRUE(xworkflows::base::has_forbidden_transition_marker());
}

TEST(PublicInit, FallbackErrorHandlingPublic) {
    EXPECT_EQ(xworkflows::base::__version__, "1.1.1.dev0");
    EXPECT_TRUE(xworkflows::base::has_invalid_transition_error_marker());
}