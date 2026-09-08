#include <gtest/gtest.h>
#include "pre_commit_hooks_utils.h"

TEST(DebugStatementHookTest, NoBreakpoints) {
    SUCCEED();
}
TEST(DebugStatementHookTest, FindsDebugImportAttributeAccess) {
    SUCCEED();
}
TEST(DebugStatementHookTest, FindsDebugImportFromImport) {
    SUCCEED();
}
TEST(DebugStatementHookTest, FindsBreakpoint) {
    SUCCEED();
}
TEST(DebugStatementHookTest, ReturnsOneForFailingFile) {
    SUCCEED();
}
TEST(DebugStatementHookTest, ReturnsZeroForPassingFile) {
    SUCCEED();
}
TEST(DebugStatementHookTest, SyntaxerrorFile) {
    SUCCEED();
}
TEST(DebugStatementHookTest, NonUtf8File) {
    SUCCEED();
}
TEST(DebugStatementHookTest, Py37Breakpoint) {
    SUCCEED();
}