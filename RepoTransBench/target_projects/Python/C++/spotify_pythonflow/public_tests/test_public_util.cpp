#include <gtest/gtest.h>
#include "pythonflow/util.h"

TEST(PublicUtil, DefaultFunc) {
    auto f = [] (int x = 13) { return x; };
    ASSERT_EQ(pythonflow::util::default_(f), 13);
}

// ... (Repeat all public util tests and logic as in test_public_util.py)