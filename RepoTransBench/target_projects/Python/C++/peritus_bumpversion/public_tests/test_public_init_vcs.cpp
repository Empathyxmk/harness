#include <gtest/gtest.h>
#include "init.h"

TEST(PublicInitVcs, KnownVcsMappingsNonGitMercurial) {
    std::map<std::string, int(*)()> vcs = get_known_vcs();
    EXPECT_TRUE(vcs.find("hg") != vcs.end());
    EXPECT_TRUE(vcs.find("svn") != vcs.end());
}

TEST(PublicInitVcs, VcsMapContentTypes) {
    std::map<std::string, int(*)()> vcs = get_known_vcs();
    for (const auto& kv : vcs) {
        EXPECT_FALSE(kv.first.empty());
    }
}

TEST(PublicInitVcs, DefaultVcsScenarios) {
    std::map<std::string, int(*)()> vcs = get_known_vcs();
    EXPECT_TRUE(vcs.find("hg") != vcs.end() || vcs.find("svn") != vcs.end());
}