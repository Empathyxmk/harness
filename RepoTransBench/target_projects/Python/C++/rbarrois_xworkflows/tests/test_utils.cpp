#include <gtest/gtest.h>
#include "xworkflows/utils.h"

// Simulate the iterclass function for C++: walk static/class variables
// For testing, we use direct struct inheritance.

TEST(UtilsTest, IterclassTraversal) {
    // Simple inheritance - properties chain
    struct A {
        static constexpr int a = 1;
    };

    struct B : public A {
        static constexpr int b = 2;
    };

    auto result = xworkflows::utils::iterclass<B>();
    // result is a map<string, int>
    ASSERT_EQ(result["a"], 1);
    ASSERT_EQ(result["b"], 2);
}

TEST(UtilsTest, IterclassOverrides) {
    struct A {
        static constexpr int foo = 3;
    };

    struct B : public A {
        static constexpr int foo = 4;
    };

    auto result = xworkflows::utils::iterclass<B>();
    ASSERT_EQ(result["foo"], 4);
}