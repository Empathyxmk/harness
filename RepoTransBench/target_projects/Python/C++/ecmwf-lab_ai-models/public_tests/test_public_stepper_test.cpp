#include <gtest/gtest.h>
#include <vector>
#include "src/ai_models/stepper.h"

TEST(PublicStepper, CustomState) {
    Stepper s(7, 3);

    std::vector<int> vals;
    // Try iteration protocol (in C++, use custom begin/end or call step explicitly)
    for (int i = 0; i < 8; ++i) {
        if (!s.done()) {
            vals.push_back(s.current());
            s.next();
        }
    }
    EXPECT_FALSE(vals.empty());
    // In case of standard pattern: should count up from 0 or 1 to 7
    int mn = *std::min_element(vals.begin(), vals.end());
    int mx = *std::max_element(vals.begin(), vals.end());
    EXPECT_TRUE(mn == 0 || mn == 1);
    EXPECT_TRUE(mx == 7 || mx == 6);

    // Test reset, if supported
    if (s.can_reset()) {
        s.reset();
        if (s.has_state()) {
            EXPECT_TRUE(s.state() == 0 || s.state() == 1);
        } else if (s.has_current()) {
            EXPECT_TRUE(s.current() == 0 || s.current() == 1);
        }
    }
}