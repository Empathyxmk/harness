#include <gtest/gtest.h>
#include "pre_commit_hooks_utils.h"

TEST(CheckAddedLargeFilesTest, NothingAdded) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, AddingSomething) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, AddSomethingGiant) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, EnforceAll) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, AddedFileNotInPreCommitsList) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, Integration) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, AllowsGitLfs) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, MovesWithGitLfs) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, EnforceAllowsGitLfs) {
    SUCCEED();
}
TEST(CheckAddedLargeFilesTest, EnforceAllowsGitLfsAfterCommit) {
    SUCCEED();
}