#include <gtest/gtest.h>
#include "init.h"
#include <map>

TEST(InitVcs, DiscardDefaultIfSpecifiedAppendAction) {
    std::map<std::string, int(*)()> vcs = get_known_vcs();
    vcs["foo"] = []() { return 2; };
    EXPECT_TRUE(vcs.find("foo") != vcs.end());
}

TEST(InitVcs, KnownVcsMapHasGit) {
    std::map<std::string, int(*)()> m = get_known_vcs();
    EXPECT_TRUE(m.find("git") != m.end());
    EXPECT_TRUE(m.find("hg") != m.end());
    EXPECT_TRUE(m.find("svn") != m.end());
}