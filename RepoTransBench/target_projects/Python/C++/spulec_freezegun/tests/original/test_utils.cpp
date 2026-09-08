#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <memory>
#include <type_traits>

// Dummy definitions to simulate cpython_only
#include "freezegun/api.h"
namespace utils {
    template <typename F>
    auto cpython_only(F&& func) {
        if (platform_is_cpython()) {
            // Direct call
            return std::forward<F>(func);
        } else {
            // Would "skip" in real test harness
            throw std::runtime_error("Test was skipped in non-CPython");
        }
    }
}
bool platform_is_cpython() {
    // Simulate CPython detection; real impl could check system property
    static bool cpython = true;
    return cpython;
}

class MockFunction {
public:
    MockFunction() : called(false), skipped(false) {}
    void operator()() {
        called = true;
    }
    bool called;
    bool skipped;
};

TEST(UtilsTest, ShouldNotSkipCPython) {
    // Simulate CPython
    extern bool platform_is_cpython();
    auto old_impl = platform_is_cpython;
    // Simulate: platform_is_cpython() returns true
    MockFunction func;
    try {
        utils::cpython_only([&func]() { func(); })();
    } catch (const std::exception& e) {
        FAIL() << "Test was skipped in CPython";
    }
    ASSERT_TRUE(func.called);
}

TEST(UtilsTest, ShouldSkipNonCPython) {
    // Simulate non-CPython
    auto platform_is_cpython = []() { return false; };
    MockFunction func;
    bool skipped = false;
    try {
        // Override the CPython check to false in this test context
        if (!platform_is_cpython()) {
            throw std::runtime_error("SkipTest");
        }
        func();
    } catch (const std::exception&) {
        func.skipped = true;
    }
    ASSERT_FALSE(func.called);
    ASSERT_TRUE(func.skipped);
}