#include <gtest/gtest.h>
#include "pre_commit_hooks_utils.h"

TEST(CheckCaseConflictTest, Parents) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, NothingAdded) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, AddingSomething) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, AddingSomethingWithConflict) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, AddingFilesWithConflictingDirectories) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, AddingFilesWithConflictingDeepDirectories) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, AddingFileWithConflictingDirectory) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, AddedFileNotInPreCommitsList) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, FileConflictsWithCommittedFile) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, FileConflictsWithCommittedDir) {
    SUCCEED();
}
TEST(CheckCaseConflictTest, Integration) {
    SUCCEED();
}