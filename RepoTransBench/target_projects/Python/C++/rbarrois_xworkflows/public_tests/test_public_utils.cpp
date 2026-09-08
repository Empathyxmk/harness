#include <gtest/gtest.h>
#include "xworkflows/utils.h"

TEST(PublicUtils, IterclassTraversalDifferent) {
    struct C {
        static constexpr int x = 10;
    };
    struct D : public C {
        static constexpr int y = 20;
    };

    auto result = xworkflows::utils::iterclass<D>();
    ASSERT_EQ(result["x"], 10);
    ASSERT_EQ(result["y"], 20);
}

TEST(PublicUtils, IterclassOverridesDifferent) {
    struct C {
        static constexpr int alpha = 7;
    };
    struct D : public C {
        static constexpr int alpha = 42;
    };

    auto result = xworkflows::utils::iterclass<D>();
    ASSERT_EQ(result["alpha"], 42);
}