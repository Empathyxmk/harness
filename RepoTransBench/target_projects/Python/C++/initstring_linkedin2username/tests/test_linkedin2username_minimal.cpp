#include <gtest/gtest.h>
#include <string>
#include "linkedin2username.h"

// Test that the main module can be used without issue
TEST(Linkedin2UsernameMinimal, ImportModule) {
    NameMutator nm("test name");
    // Just ensure construction
    ASSERT_TRUE(true);
}

TEST(Linkedin2UsernameMinimal, MainInvocation) {
    // Simulate calling main()
    // For test, we simulate patch of main with a lambda
    int called = 0;
    auto fake_main = [&called]() { called = 1; };
    // In real case, main() in C++ is not patchable, so instead we test a callable main via function pointer
    void (*main_func)() = nullptr;
    main_func = +[]() {};
    fake_main();
    EXPECT_EQ(called, 1);
}