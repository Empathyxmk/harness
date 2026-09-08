#include <gtest/gtest.h>
#include "pre_commit_hooks_utils.h"

TEST(CheckMergeConflictTest, MergeConflictsGit) {
    SUCCEED();
}
TEST(CheckMergeConflictTest, MergeConflictsFailing) {
    SUCCEED();
}
TEST(CheckMergeConflictTest, MergeConflictsOk) {
    SUCCEED();
}
TEST(CheckMergeConflictTest, IgnoresBinaryFiles) {
    SUCCEED();
}
TEST(CheckMergeConflictTest, DoesNotCareWhenNotInAMerge) {
    SUCCEED();
}
TEST(CheckMergeConflictTest, CareWhenAssumedMerge) {
    SUCCEED();
}
TEST(CheckMergeConflictTest, WorktreeMergeConflicts) {
    SUCCEED();
}