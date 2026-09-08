#include "gtest/gtest.h"
#include "lib/scent.h"
#include <string>

TEST(TestScent, PyFilesValidator) {
    EXPECT_TRUE(py_files("abc.py"));
    EXPECT_FALSE(py_files(".abc.py"));
    EXPECT_FALSE(py_files("abc.txt"));
}

TEST(TestScent, ExecuteKoansRuns) {
    bool systemCalled = false;
    std::string systemCmd;
    set_system_fn([&](const std::string& cmd) {
        systemCalled = true;
        systemCmd = cmd;
        return 0;
    });
    execute_koans();
    EXPECT_TRUE(systemCalled);
    EXPECT_NE(systemCmd.find("contemplate_koans"), std::string::npos);
}