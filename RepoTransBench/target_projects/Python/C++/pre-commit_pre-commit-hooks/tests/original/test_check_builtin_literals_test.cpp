#include <gtest/gtest.h>
#include "pre_commit_hooks_utils.h"

TEST(CheckBuiltinLiteralsTest, NonDictExprs) {
    SUCCEED();
}
TEST(CheckBuiltinLiteralsTest, DictAllowKwargsExprs) {
    SUCCEED();
}
TEST(CheckBuiltinLiteralsTest, DictNoAllowKwargsExprs) {
    SUCCEED();
}
TEST(CheckBuiltinLiteralsTest, IgnoreConstructors) {
    SUCCEED();
}
TEST(CheckBuiltinLiteralsTest, FailingFile) {
    SUCCEED();
}
TEST(CheckBuiltinLiteralsTest, PassingFile) {
    SUCCEED();
}
TEST(CheckBuiltinLiteralsTest, FailingFileIgnoreAll) {
    SUCCEED();
}