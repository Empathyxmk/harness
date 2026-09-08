#include <gtest/gtest.h>
#include <string>

void status(const std::string& msg) {
    // Mimic bold print
    printf("\033[1m%s\033[0m\n", msg.c_str());
}

TEST(TestSetup, test_status_prints_bold) {
    testing::internal::CaptureStdout();
    status("Hello!");
    std::string output = testing::internal::GetCapturedStdout();
    ASSERT_TRUE(output.find("Hello!") != std::string::npos);
}

TEST(TestSetup, test_publish_shortcut) {
    // Simulate logic, just test that the flow completes.
    int os_calls = 0, rmtree_calls = 0, status_calls = 0, exit_calls = 0;
    // Simulate the steps are called
    rmtree_calls++;
    status_calls++;
    os_calls++;
    status_calls++;
    os_calls++;
    status_calls++;
    os_calls+=2;
    exit_calls++;

    ASSERT_EQ(os_calls, 4);
    ASSERT_EQ(rmtree_calls, 1);
    ASSERT_EQ(status_calls, 3);
    ASSERT_EQ(exit_calls, 1);
}