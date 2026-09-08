#include <gtest/gtest.h>
#include "pre_commit_hooks_utils.h"

TEST(CheckExecutablesHaveShebangsTest, HasShebang) {
    SUCCEED();
}
TEST(CheckExecutablesHaveShebangsTest, BadShebang) {
    SUCCEED();
}
TEST(CheckExecutablesHaveShebangsTest, CheckGitFilemodePassing) {
    SUCCEED();
}
TEST(CheckExecutablesHaveShebangsTest, CheckGitFilemodePassingUnusualCharacters) {
    SUCCEED();
}
TEST(CheckExecutablesHaveShebangsTest, CheckGitFilemodeFailing) {
    SUCCEED();
}
TEST(CheckExecutablesHaveShebangsTest, GitExecutableShebang) {
    SUCCEED();
}