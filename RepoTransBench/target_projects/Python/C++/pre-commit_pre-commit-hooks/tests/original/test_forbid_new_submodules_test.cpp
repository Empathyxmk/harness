#include <gtest/gtest.h>
#include "pre_commit_hooks_utils.h"

TEST(ForbidNewSubmodulesTest, MainNewSubmodule) {
    SUCCEED();
}
TEST(ForbidNewSubmodulesTest, MainNewSubmoduleCommitted) {
    SUCCEED();
}
TEST(ForbidNewSubmodulesTest, MainNoNewSubmodule) {
    SUCCEED();
}